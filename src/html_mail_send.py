import smtplib, os, datetime, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

FROM_ADDRESS = os.environ['FROM_ADDRESS']
MY_PASSWORD  = os.environ['hotmail_pass']
#TO_ADDRESS   = (os.environ['TO_ADDRESS'], os.environ['TO_ADDRESS3'])
TO_ADDRESS   = (os.environ['TO_ADDRESS3'],)
buf = os.environ['TO_ADDRESS_TEAM'] + ',' + os.environ['TO_ADDRESS']
BCC_ADDRESS  = tuple(buf.split(','))

#CHARSET      = "ISO-2022-JP"
CHARSET      = "utf-8"

def __create_html_message(to, sbj, html, bcc):
    
    msg = MIMEMultipart('alternative')

    if type(to) is tuple or type(to) is list:
        msg['To'] = ",".join(to)
    else:
        msg['To'] = to
    
    if bcc != ():
        msg['Bcc'] = ",".join(bcc)

    msg['Subject'] = sbj
    msg['From'] = FROM_ADDRESS
    cset = 'utf-8'
    
    text = 'This is a html mail.'

    part_t = MIMEText(text, 'plain', cset)
    part_h = MIMEText(html, 'html', cset)

    msg.attach(part_t)
    msg.attach(part_h)

    return msg
    
def __send(msg):
    smtpobj = smtplib.SMTP('smtp.live.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.send_message(msg = msg)
    smtpobj.close()

omit = object()
def html_mailing(subject, html, to=omit):
    if to is omit:
        to = TO_ADDRESS
        bcc = BCC_ADDRESS
    elif to == 'debug':
        to = (os.environ['TO_ADDRESS'],)
        bcc = ()

    if html != '':
        msg = __create_html_message(to, subject, html, bcc)
        __send(msg)

if __name__ == '__main__':
    html_mailing('html_mail_test','a')