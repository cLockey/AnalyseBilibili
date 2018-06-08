# -*-coding:utf8-*-

import requests
import sqlite3
import json
import datetime
import time
import random


# head = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Referer': 'http://space.bilibili.com/45388',
#     'Origin': 'http://space.bilibili.com',
#     'Host': 'space.bilibili.com',
#     'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
#     'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
# }

def get_users():
    begin = 1
    end = 10
    for i in range(begin, end):
        space_url = "https://space.bilibili.com/" + str(i) + "/#/"
        get_info_url = "https://space.bilibili.com/ajax/member/info" 

        head = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'Referer': 'https://space.bilibili.com/' + str(i) + '?from=search&seid=' + str(random.randint(10000, 50000))
        }
        form_data = {
            #'_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
            'mid': str(i)#url.replace('https://space.bilibili.com/', '')
        }
        jscontent = requests.session().post('http://space.bilibili.com/ajax/member/GetInfo', headers=head, data=form_data).text
        jsDict = json.loads(jscontent)
        statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
        if statusJson == True:
            if 'data' in jsDict.keys():
                jsData = jsDict['data']
                print(jsData['name'])
        else:
            print('no data now')




if __name__ == "__main__":
    # TODO
    get_users()
    pass