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

def outlook(subject, contents):
    outlook = win32com.client.Dispatch("Outlook.Application")
    message = outlook.CreateItem()
    message.DeleteAfterSubmit = True
    message.Subject = subject
    message.Body = contents.decode()
    message.To = tgt_accts[0]
    message.Send()

if __name__ == '__main__':
    plain_email('test2 message', 'attack at dawn.')