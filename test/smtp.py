import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import os


def send_mail(send_from, send_to, subject, message, mtype='plain', files=[],
              server="localhost", port=587, username='', password='',
              use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        mtype (str): choose type 'plain' or 'html'
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    '''
    msg.attach(MIMEText(message, mtype))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment', filename=Path(path).name)
        msg.attach(part)
    '''
    smtp = smtplib.SMTP(server, port)

    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


id = "Developer"
pw = "dnjsgh1356P"
email = "daniel__p@naver.com"

# 네이버의 경우 server='smtp.naver.com'
server_setting={
    "google":'smtp.gmail.com',
    "naver":'smtp.naver.com'
}

send_mail(send_from=email, send_to=["parkwonho94@gmail.com","gnvid35@naver.com"],
          subject='smtp 테스트 발송 메세지 입니다', message=f'<h1>안녕하세요</h1>{id}입니다', #files=['temp.txt'],
          mtype='html', server=server_setting["naver"], username=email, password=pw)