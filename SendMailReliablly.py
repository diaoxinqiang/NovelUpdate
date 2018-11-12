# -*- coding:utf-8 -*-
from send_email import send_email


# from SimpleDBUsingFS import SimpleDBUsingFS
import utf8logger
from utf8logger import ERROR, INFO

class SendMailReliablly:
    """可靠邮件发送器，发送失败会自动保存进数据库里，下次激活时自动重发"""

    def __init__(self, dbLocation, tableName, dbClass):
        # 为发送失败的邮件建立数据库
        self.db = dbClass(dbLocation, tableName, ['to_whom_list', 'title', 'content'])
        self.delimiter = '$^&'

    def send(self, to_whom_list, title, content):
        """发送邮件的主体逻辑：
        1）待发送邮件=以前发送失败的+现在要发送的
        2）逐封邮件发送（可能需要调整一个发送间隔，因为太快连续发送，会导致邮件服务器拒绝服务；
        3）收集这一次发送失败的邮件；
        4）清空原来的“发送失败”数据库，把新的数据保存进去。
        """
        emails_to_send = self.db.get_all()  # 以前发送失败的邮件
        if len(emails_to_send) > 0:
            INFO('有{0}封发送失败的邮件'.format(len(emails_to_send)))
        # 由于收件人是一个列表，对于数据库的一个字段，所以需要存入时先序列化为字符串，读取则反过来
        for i in range(0, len(emails_to_send)):
            emails_to_send[i][0] = emails_to_send[i][0].splite(self.delimiter)
        emails_to_send.append([to_whom_list, title, content])
        now_fail_emails = []  # 当前发送失败的邮件列表

        for email in emails_to_send:
            try:
                result = send_email(email[0], email[1], email[2])
            except Exception as e:
                result = {str(e)}
                ERROR('smtplib error happend.......................')

            ERROR('send_result:', result)
            if len(result) > 0:
                now_fail_emails.append(email)

        self.db.delete_all()
        ERROR("fail??? ", len(now_fail_emails))
        for email in now_fail_emails:
            email[0] = self.delimiter.join(email[0])
            self.db.insert(email)
        return len(now_fail_emails) == 0
