# -*- coding:utf-8 -*-
import re

import utf8logger
from SendMailReliablly import SendMailReliablly
from SimpleDBUsingSqlite3 import SimpleDBUsingSqlite3
from SinglePageSpider import SinglePageSpider
from config import *

from utf8logger import ERROR, INFO


class UpdateMonitorBaseClass:
    """抽象监测更新并发送邮件的逻辑，成为一个类，只需要简单传入参数即可塑造一个业务！"""

    def __init__(self, email_send_list, name, url, pattern, dbClass=SimpleDBUsingSqlite3,
                 coding='utf-8', tips='章', columns=['link_address'], url_prefix=None):
        self.email_send_list = email_send_list
        self.name = name
        self.url = url
        self.dbClass = dbClass
        self.db = self.dbClass(DATA_ABS_PATH + '/NovelUpdate_data', self.name, columns)
        self.reliableEmailSender = SendMailReliablly(DATA_ABS_PATH + '/NovelUpdate_fail', self.name,
                                                     self.dbClass)
        self.pattern = re.compile(pattern, re.I)
        self.coding = coding
        self.tips = tips
        self.url_prefix = url_prefix

        self.checkUpdate()

    def getTargetContent(self):
        """获取指定页面的目标内容：
        1）指定页面由SinglePageSpider获取；
        2）目标内容由正则表达式匹配得到。

        Returns: a list of update chapters' relative path and its title
        such as [('http://dazhuzai.net.cn/dazhuzai-1309.html', 'title 1'), ]
        """
        try:
            page = SinglePageSpider().getPage(self.url, self.coding)
            result = re.findall(self.pattern, page)
            if result:
                if self.url_prefix:
                    for i in range(len(result)):
                        chapter_url = self.url_prefix + result[i][0]
                        if len(result[i]) >= 3:
                            data = result[i][1:len(result[i])]
                            chapter_title = '  '.join(reversed(data))
                        else:
                            chapter_title = result[i][1]
                        result[i] = (chapter_url, chapter_title)
                INFO('正则匹配成功:{0}{1}'.format(len(result),self.tips))
                return result
            else:
                ERROR('正则匹配失败')
                return None
        except Exception as e:
            ERROR('获取网页失败：')
            ERROR(e)
            return None

    def checkUpdate(self):
        """监测更新的主体逻辑：
        1）获取当前的页面内容；
        2）与数据库里保存的数据比对，找出更新的数据；
        3）生成通知的邮件内容，扔给“可靠邮件发送器”发送
        """
        INFO('爬取{0}章节目录中...'.format(self.name))
        currentTies = self.getTargetContent()
        INFO('获取 {0}章节成功'.format(self.name))
        if currentTies is None:
            return False

        updateTies = []
        for (tie, title) in currentTies:
            result = self.db.find([tie])
            if not result:
                updateTies.append((tie, title))
                self.db.insert([tie])

        if len(updateTies) == 0:
            return False
        INFO('更新了{0}{1}'.format(len(updateTies), self.tips))
        to_whom_list, title, content = self.generate_noticification(updateTies)
        send_result = self.reliableEmailSender.send(to_whom_list, title, content)
        if send_result:
            INFO('发送邮件成功')
        else:
            INFO('发送邮件失败，待重发')
        return True

    def generate_noticification(self, new_contents):
        """generate email to notify the users about the new contents"""
        if new_contents is not None and len(new_contents) > 0:
            mail_title = '{0}更新了{1}{2}'.format(self.name, len(new_contents), self.tips)
            if len(new_contents) == 1:
                mail_title += ':{0}'.format(new_contents[0][1])
            content = ''
            for (url, title) in new_contents:
                content += '{0}\n{1}\n\n'.format(title, url)
            return [self.email_send_list, mail_title, content]
        else:
            return [None] * 3
