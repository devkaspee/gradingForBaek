import Parsing
import Slack
from slacker import Slacker
import Data

userids = {"kaspee": "임호준", "bryan980908": '정현엽'}


def main():
    db = Data.DB()
    slack_token = 'xoxb-520020160421-519719784739-zWONuvzfO5C1aiN79WF64oZM'
    slack = Slacker(slack_token)
    not_submit_user = []

    for i in userids:
        test = Parsing.Parsing(i)
        test.status()
        if test.getNum() < 2:
            not_submit_user.append(i)

    slack.chat.post_message(channel='#general', text='📑 <!everyone> 문제 검사가 종료되었습니다. ', attachments=[{
        "text": '전체 인원 %d명중, 제출은 %d명 미제출은 %d명입니다.' % (
            len(userids), len(userids) - len(not_submit_user), len(not_submit_user))
    }])
    slack.chat.post_message(channel='#general', text='📬 제출')
    for i in userids:
        test = Parsing.Parsing(i)
        test.status()
        slacker = Slack.Slack(test.getDictList(), userids[i], i)
        closer = slacker.getAttaches()
        if closer == None:
            pass
        elif len(closer) == 1:
            try:
                slack.chat.post_message('#general', attachments=closer)
                temps = closer[0]["text"] # 반드시 필요하니 지우지 말 것
                db.submit(i)
            except:
                pass
    slack.chat.post_message(channel='#general', text='👮‍♀️ 미제출')
    for i in not_submit_user:
        db.un_submit(i)
        print(i, str(500 * (2 ** (int(db.read(i)[1])-1))) + "원이 누적되었습니다. (총계: " + str(db.read(i)[0]) + "원, " + str(
            db.read(i)[1]) + ")")
        slack.chat.post_message(channel='#general', attachments=[{
            "color": "#f03e3e",
            "author_name": userids[i] + "(" + i + ")",
            "author_link": "https://www.acmicpc.net/status?problem_id=&user_id=" + i + "&language_id=-1&result_id=4",
            "text": "벌금 " + str(500 * (2 ** (int(db.read(i)[1]) - 1))) + "원이 누적되었습니다. (총계: " + str(
                db.read(i)[0]) + "원, " + str(db.read(i)[1]) + "일차)"
        }])

    db.closes()

def Test():
    slack_token = 'xoxb-520020160421-519719784739-zWONuvzfO5C1aiN79WF64oZM'
    slack = Slacker(slack_token)
    slack.chat.post_message(channel='#general', text = "테스트 중입니다.")

Test()
