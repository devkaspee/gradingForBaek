import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import re


class Parsing:
    def __init__(self, userid):
        self.DictList = []
        self.userid = userid
        self.num = 0
        #   0 ~ 2까지는 갯수, 3부터는 3개 이상
        Dataline = []
        #   [0] 채점 번호 [1] 아이디 [2] 문제 번호 [3] 채점 결과
        #   [4] 메모리 (KB) [5] 시간(ms) [6] 언어 [7] 코드 길이
        #   [8] 제출 시간
        req = requests.get('https://www.acmicpc.net/status?user_id=' + userid + '&result_id=4').text
        soup = BeautifulSoup(req, 'html.parser')
        self.lines = soup.find("tbody").find_all('tr')  # 최대 20개 문제에 대한 line들을 저장

        return

    def status(self):
        count = 0
        for line in self.lines:
            Dataline = line.find_all('td')
            Dates = Dataline[8].find('a')['title']
            matches = re.match("(\\d+)년 (\\d+)월 (\\d+)일 (\\d+)시 (\\d+)분 (\\d+)초", Dates)
            times = [matches.group(i) for i in range(1, 7)]
            nowtime = list(map(str, list(map(int, str(datetime.now()).split()[0].split('-')))))
            if nowtime == times[0:3]:
                if self.checkOverlab(Dataline[2].text):
                    count += 1
                    self.setDictList(Dataline[2].text, Dates)
            else:
                self.num = count
                return

            self.num = count


    def checkOverlab(self, number):
        checkSet = set()
        reqForCheck = requests.get(
            'https://www.acmicpc.net/status?problem_id=' + str(number) + '&user_id='
            + self.userid + '&language_id=-1&result_id=4&from_problem=1').text
        soupForCheck = BeautifulSoup(reqForCheck, 'html.parser')
        linesForCheck = soupForCheck.find("tbody").find_all('tr')
        for linestemp in linesForCheck:
            numtemp = linestemp.find_all('td')
            checkSet.add(numtemp[8].find('a')['title'])

        if len(checkSet) != 1:
            return False
        else:
            return True

    def setDictList(self, number, Dates):
        dicts = {}
        dicts['solve_number'] = str(number)
        reqForDict = requests.get('https://www.acmicpc.net/problem/' + str(number)).text
        dicts['solve_title'] = str(BeautifulSoup(reqForDict, 'html.parser').select_one('#problem_title').text)
        self.DictList.append(dicts)
        dicts['solve_time'] = self.parse_date(Dates, timezone(timedelta(hours=9))).timestamp()
        return

    def getDictList(self):
        return self.DictList

    def getLines(self):
        return self.lines

    def getNum(self):
        return self.num

    def parse_date(self, date_text: str, tzinfo: timezone):
        matches = re.match("(\\d+)년 (\\d+)월 (\\d+)일 (\\d+)시 (\\d+)분 (\\d+)초", date_text)
        times = [matches.group(i) for i in range(1, 7)]

        return datetime(*map(int, times), tzinfo=tzinfo)


if __name__ == '__main__':
    test = Parsing('rjsdn4545')
    test.status()
    print(test.getNum())
    print(test.getDictList())
