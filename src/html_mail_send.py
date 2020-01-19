import smtplib, os, datetime, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

FROM_ADDRESS = os.environ['FROM_ADDRESS']
MY_PASSWORD  = os.environ['hotmail_pass']
TO_ADDRESS   = (os.environ['TO_ADDRESS'], os.environ['TO_ADDRESS3'])

#CHARSET      = "ISO-2022-JP"
CHARSET      = "utf-8"

def __create_html_message(to, sbj, html):
    
    msg = MIMEMultipart('alternative')

    if type(to) is tuple or type(to) is list:
        msg['To'] = ",".join(to)
    else:
        msg['To'] = to

    msg['Subject'] = sbj
    msg['From'] = FROM_ADDRESS
    
    text = 'This is a html mail.'

    part_t = MIMEText(text, 'plain')
    part_h = MIMEText(html, 'html')

    msg.attach(part_t)
    msg.attach(part_h)

    return msg
    
def __send(from_adr, to_adr, msg):
    smtpobj = smtplib.SMTP('smtp.live.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_adr, to_adr, msg.as_string())
    smtpobj.close()

omit = object()
def html_mailing(subject, html, to=omit):
    if to is omit:
        to = TO_ADDRESS
    
    if html != '':
        msg = __create_html_message(to, subject, html)
        __send(FROM_ADDRESS,to, msg)

if __name__ == '__main__':
    html_mailing('html_mail_test','a')