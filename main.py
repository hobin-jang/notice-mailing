import schedule 
import time
from bs4 import BeautifulSoup
import requests
import datetime
from dataclasses import dataclass
import mail
from dotenv import load_dotenv
import os

# 필요한 데이터 타입 지정
@dataclass
class Information:
    title: str
    url : str 
    date : str

# .env에서 설정 가져오기
load_dotenv()
sender = os.environ.get("sender")
password = os.environ.get("password")
receiver1 = os.environ.get("receiver1")
receiver2 = os.environ.get("receiver2")
receiver3 = os.environ.get("receiver3")

# 수신자 모음
receiverList = [receiver1,receiver2,receiver3]

# 메일 양식
def mailForm(title, url, date) : 

    mailTitle = "[정보보호대학원 공지사항 메일 알림] " + title

    msg1 = "정보보호대학원의 새로운 공지 사항 메일입니다.\n\n"
    msg2 = "제목 : " + title + "\n\n"
    msg3 = "링크 : " + url + "\n\n"
    msg4 = "등록일 : " + date + "\n\n"

    mailContent = msg1 + msg2 + msg3 + msg4

    return mailTitle, mailContent

# 공지글 가져와서 메일 보내기
# prevInfoList : 메일 보냈던 것 체크용
def getInfoAndSendMail(prevInfoList) : 

    print("start getting information")

    # 정보보호대학원 공지사항 1페이지
    url = "https://gss.korea.ac.kr/ime/commu/notice.do"
    # 공지 페이지 가져오기
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # 공지사항 글 테이블
    board = soup.find("section", id="jwxe_main_content")
    tbody = board.find("tbody")

    # 오늘 날짜 계산 (ex. 2022.01.01)
    today = datetime.datetime.now().strftime("%Y.%m.%d")

    # 테이블 내의 각 공지
    infoList = []
    trList = tbody.find_all("tr")
    for tr in trList :
        tdList = tr.find_all("td")
        # 2번째에 게시글 정보, 5번째에 날짜
        a = tdList[1].find("a")
        title = a.get_text()
        href = a["href"]
        date = tdList[4].get_text()

        # 오늘 새로 올라온 공지 + 아직 메일 안 보낸 거
        if today == date and title not in prevInfoList :     
            infoList.append(Information(title, url + href, date))
            prevInfoList.append(title)

    # 새로운 공지글 있음
    if len(infoList) != 0:
        for info in infoList:
            # 메일 보내기
            mailTitle, mailContent = mailForm(info.title, info.url, info.date)
            mail.send_mail(sender, receiverList, sender, password, mailTitle, mailContent)
            # 공지 여러 개면 1초 간격으로 보내기
            time.sleep(1)
            #print("send mail end : ", info)

# prevInfoList 초기화
def resetPrevInfoList(prevInfoList):
    prevInfoList.clear()

# 서버 시간 설정
# 공지 탐색은 1시간에 한 번 씩
# 매일 00:00에 prevInfoList 초기화
prevInfoList = []
schedule.every().hour.do(getInfoAndSendMail, prevInfoList)
schedule.every().day.at("00:00").do(resetPrevInfoList, prevInfoList)

# 메일 서비스 시작!!!!
while True:
    schedule.run_pending()
    time.sleep(1)
    # 1초마다 돌면서 schedule 체크 (시간 되면 schedule에서 실행 자동으로 함)
