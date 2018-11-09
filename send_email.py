# -*- coding: utf-8 -*-
import smtplib
import email.mime.multipart
import email.mime.text

EMAIL_HOST = '767470799@qq.com'  # your email address
EMAIL_PASS = 'itdgyfictwgobbii'  # your email account password
# EMAIL_PASS = '*'   # your email account password
SMTP_SERVER = 'smtp.qq.com'  # your email smtp server domain name
SMTP_PORT = '465'  # smtp protocol use port 465 to send email


# 如果返回值为空{}，则表示全部发送成功，否则……
def send_email(to_whom_list, title, content):
    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = EMAIL_HOST
    msg['to'] = ";".join(to_whom_list)
    msg['subject'] = title
    txt = email.mime.text.MIMEText(content)
    msg.attach(txt)

    have_exception = False
    try:
        smtp = smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT)
        smtp.login(EMAIL_HOST, EMAIL_PASS)
        result = smtp.sendmail(EMAIL_HOST, to_whom_list, str(msg))
    except Exception as e:
        print('exception when send_email...')
        print(e)
        have_exception = True
    finally:
        smtp.quit()
        if have_exception:
            print('finally raise e: {0}'.format(str(e)))
            raise e
        else:
            print('finally no exception raise')
    return result

# Example tl use the function:
# send_email(['767470799@qq.com'], 'Testing title', 'I am a test and I am testing the send_email function')
