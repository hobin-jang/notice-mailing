import smtplib
from email.mime.text import MIMEText
import time

def smtp_setting(email, password) : 
    mailType = "smtp.naver.com"
    port = 587
    # gmail : TLS 587 port => gmail은 써드 파티로 메일 보내는 거 막힘
    # outlook : SSL 465 port
    # naver : SSL 465 port, 587 TLS

    # smtp 세션
    smtp = smtplib.SMTP(mailType, port)
    smtp.set_debuglevel(True)

    # smtp 로그인
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email, password)

    return smtp 

def send_mail(sender, receiverList, email, password, subject, content) : 
    
    try:
        # 세션 연결
        smtp = smtp_setting(email, password)

        # 여러 명한테 보내기
        for receiver in receiverList : 
            # 메일 데이터
            msg = MIMEText(content)
            msg['Subject'] = subject 
            msg['From'] = sender 
            msg['To'] = receiver

            # 1초 간격 메일 보내기
            smtp.sendmail(sender, receiver, msg.as_string())
            time.sleep(1)

    except Exception as e:
        print('error : ', e)
    finally:
        if smtp is not None:
            # 세션 종료
            smtp.quit()

# example
# send_mail(sender, receiver, sender, password, "제목", "내용")