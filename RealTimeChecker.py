# -*- coding:utf-8 -*-
import sys
from UpdateMonitorBaseClass import UpdateMonitorBaseClass
from SimpleDBUsingFS import SimpleDBUsingFS
from SimpleDBUsingSqlite3 import SimpleDBUsingSqlite3


def main(args):
    email_send_list = ['767470799@qq.com']
    dazhuzai = UpdateMonitorBaseClass(
        email_send_list,
        '《剑来》',
        'http://book.zongheng.com/showchapter/672340.html',
        '<a.*?href=\"http:\/\/book.zongheng.com\/chapter\/672340/(.*?)\" target=\"_blank\" title=\"(.*?)\">(.*?)<\/a>',
        url_prefix='http://book.zongheng.com/chapter/672340/',
        tips='章',
    )
    # dadaochaotian = UpdateMonitorBaseClass(
    #     email_send_list,
    #     '《大道朝天》',
    #     'https://book.qidian.com/info/1010496369#Catalog',
    #     '<a href="\/\/vipreader.qidian.com\/chapter\/1010496369\/(.*?)\" .*?title=\"(.*?)\">(.*?)<\/a>',
    #     url_prefix='http://vipreader.qidian.com/chapter/1010496369/',
    #     tips='章',
    # )


if __name__ == '__main__':
    exit(main(sys.argv[1:]))
