import smtplib
import time
import win32com.client

smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_acct = 'me@example.com'
smtp_passwd = 'seKret'
tgt_accts = ['me@other.com']


def plain_email(subject, contents):
    message = f'Subject: {subject}\nFrom {smtp_acct}\n'
    message += f'To: {tgt_accts}\n\{contents.decode()}'
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_acct, smtp_passwd)

    #server.set-debuglevel(1)
    server.sendmail(smtp_acct, tgt_accts, message)
    time.sleep(1)
    server.quit()
