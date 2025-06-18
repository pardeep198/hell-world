import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

def check_appointment(url, session=None):
    session = session or requests.Session()
    resp = session.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    return "No appointments available" not in soup.text

def send_email(from_addr, to_addr, password, body):
    msg = MIMEText(body)
    msg['Subject'] = 'Visa appointment available'
    msg['From'] = from_addr
    msg['To'] = to_addr
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
        s.login(from_addr, password)
        s.sendmail(from_addr, [to_addr], msg.as_string())

def monitor(url, email_cfg, check_interval=3600):
    session = requests.Session()
    while True:
        if check_appointment(url, session):
            send_email(email_cfg['from'], email_cfg['to'], email_cfg['password'],
                       f'Appointment available at {url}')
            break
        time.sleep(check_interval)

if __name__ == '__main__':
    TARGET_URL = 'https://example.com/visa'  # TODO: update with real URL
    EMAIL_CFG = {
        'from': 'you@example.com',
        'to': 'you@example.com',
        'password': 'EMAIL_PASSWORD'
    }
    monitor(TARGET_URL, EMAIL_CFG)
