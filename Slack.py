class Slack():
    def __init__(self, dict, username, userid):

        self.DictList = dict
        self.attaches = []
        self.username = username
        self.userid = userid

    def getDictList(self):
        return self.DictList

    def getAttaches(self):
        line = self.getDictList()
        if len(line) == 0:
            return

        if len(line) >= 1:
            self.attaches += [{"color": "#37b24d",
                                "author_name": self.username + "(" + self.userid + ")",
                                "author_link": "https://www.acmicpc.net/status?problem_id=&user_id=" + self.userid + "&language_id=-1&result_id=4",
                                "title": str(line[0]['solve_number']) + "번 " + str(line[0]['solve_title']),
                                "title_link": "https://boj.kr/" + str(line[0]['solve_number']),
                                "footer": "Baekjoon Online Judge",
                                "footer_icon": "https://www.acmicpc.net/favicon-32x32.png",
                                "ts": line[0]['solve_time']}]

            if len(line) > 1:
                self.attaches[0]['text'] = "\t 외에도 " + str(len(line) - 1) + "개의 문제를 풀었습니다."

            return self.attaches
