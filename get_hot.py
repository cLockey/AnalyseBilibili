# -*-coding:utf8-*-

import requests
import sqlite3
import json
import datetime
import time
import random
from login import Login
#import sys
#from importlib import reload

#reload(sys)  
#sys.setdefaultencoding('utf-8')  

header = {
    'Referer': 'https://t.bilibili.com/?tab=1000',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    
    # 'Accept': 'application/json, text/plain, */*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6,ca;q=0.5',
    # 'Connection': 'keep-alive',
    # #'Cookie': 'l=v; finger=edc6ecda; LIVE_BUVID=AUTO6415282736010851; fts=1528273622; sid=8wlapccd; DedeUserID=17486373; DedeUserID__ckMd5=ec15607bb9522c5c; SESSDATA=2aea00a0%2C1530865609%2C97f99c36; bili_jct=b870ce10ebf12d5717bb8e57ab40c40d; _dfcaptcha=2005c4acf2085ba5c7141ae1a8fe956f; bp_t_offset_17486373=125729012904691804; UM_distinctid=163d46b7658500-04380da18b4fc3-3c3c520d-1fa400-163d46b7659461; buvid3=38B95E3A-7426-405F-ADB3-326985B7BFFD20808infoc; rpdid=owiwopkxpidosiqiqwmxw; CURRENT_QUALITY=80; im_local_unread_17486373=0; im_notify_type_17486373=0',
    # 'Host': 'api.vc.bilibili.com',
    # 'Origin': 'https://t.bilibili.com',
    # 'Referer': 'https://t.bilibili.com/?tab=1000',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}

format_data = {
    'uid': '17486373',
    'page': '1'
}

before_data_0 = {
    '0000171528376188234https://t.bilibili.com/?tab=1000|444.41.selfDef.page_hotshow||1528376188233|0|0|573x974|1|{"event":"page_hotshow","value":{"tab_type":"hot"}}' : ''
}
before_data_1 = {
    '0005021528376188234https://t.bilibili.com/?tab=1000|444.41.selfDef.page_hotshow||1528376188233|0|0|573x974|1|{"event":"page_hotshow","value":{"tab_type":"hot"}}' : ''
}

before_get_hot_url_0 = '''https://data.bilibili.com/log/web?000017{TimeStamp}https%3A%2F%2Ft.bilibili.com%2F%3Ftab%3D1000|
    444.41.selfDef.page_hotshow||{TimeStamp}|0|0|573x974|1|{%22event%22:%22page_hotshow%22,%22value%22:{%22tab_type%22:%22hot%22}}'''    
before_get_hot_url_1 = '''https://data.bilibili.com/log/web?000502{TimeStamp}https%3A%2F%2Ft.bilibili.com%2F%3Ftab%3D1000|
    444.41.selfDef.page_hotshow||{TimeStamp}|0|0|573x974|1|{%22event%22:%22page_hotshow%22,%22value%22:{%22tab_type%22:%22hot%22}}'''
get_hot_url_base = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/recommend'

def request_before():
    curr_time = time.time()*1000
    print('curr_time: {}'.format(curr_time))
    url0 = 'https://data.bilibili.com/log/web'#before_get_hot_url_0.replace('{TimeStamp}', str(int(curr_time)))
    url1 = 'https://data.bilibili.com/log/web'#before_get_hot_url_1.replace('{TimeStamp}', str(int(curr_time)))
    print(url0)
    print(url1)
    response = requests.get(url0, params=before_data_0)
    print(response.url)
    response = requests.get(url1, params=before_data_1)

def get_hot_page_num():
    response = requests.get(get_hot_url_base)
    #print(response.headers)
    json_hot = json.loads(response.text)
    hot_data = json_hot['data']
    total_page = hot_data['total_page']
    print("total_page: ", total_page)
    return int(total_page)

def get_hot_datas_of_page(page_idx):
    print('===============================Page {}================================'.format(page_idx))
    format_data['page'] = str(page_idx)
    response = requests.session().get(get_hot_url_base, params=format_data)# + str(page_idx))
    #print(response.headers)
    json_hot = json.loads(response.text)
    #print(response.text)
    hot_data = json_hot['data']
    total_page = hot_data['total_page']
    cards = hot_data['cards']
    print("cards_num: ", len(cards))
    hot_datas = []
    for card in cards:
        hot_datas.append(format_card(card))
    return hot_datas

def format_card(card_json):
    card = card_json
    like_cnt = card['desc']['like']
    repost_cnt = card['desc']['repost']
    card_info = json.loads(card['card'])
    reply_cnt = 0
    card_type = card['desc']['type']
    #card_type: 1：转发，2：图文，4：纯文字，8，投稿视频（常规视频）16: 小视频，64：文章, 
    if card_type & (1+2+4+16) != 0:
        reply_cnt = card_info['item']['reply']
    elif card_type & (8+64) != 0:
        reply_cnt = card_info['stats']['reply']
    elif card_type & 256 != 0:
        reply_cnt = card_info['replyCnt']

    local_time = time.localtime(card['desc']['timestamp'])
    post_date = time.strftime("%Y-%m-%d %H:%M:%S",local_time)
    user_profile = card['desc']['user_profile']
    uid = user_profile['info']['uid']
    uname = user_profile['info']['uname']
    print('uid: {}, uname: {}, card_type: {}, like_cnt:{}, repost_cnt: {}, reply_cnt: {}, post_date: {}'
        .format(uid, uname, card_type, like_cnt, repost_cnt, reply_cnt, post_date))

    hot_data = {}
    hot_data['uid'] = uid
    hot_data['uname'] = uname
    hot_data['card_type'] = card_type
    hot_data['like_cnt'] = like_cnt
    hot_data['repost_cnt'] = repost_cnt
    hot_data['reply_cnt'] = reply_cnt
    hot_data['post_date'] = post_date
    return hot_data

def create_table():
    conn = sqlite3.connect('bilibili.db')
    cursor = conn.cursor()    
    cursor.execute('''create table if not exists hot_data (id integer primary key autoincrement, 
        uid varchar(20), 
        uname varchar(50), 
        card_type integer, 
        like_cnt integer,
        repost_cnt integer,
        reply_cnt integer,
        post_date datetime,
        spide_date datetime); ''')
    conn.commit()
    conn.close()

def save_hot_datas(hot_datas):
    conn = sqlite3.connect('bilibili.db')
    cursor = conn.cursor()  
    local_date = time.localtime(time.time())
    spide_date = time.strftime("%Y-%m-%d %H:%M:%S",local_date)
    for data in hot_datas:        
        #cursor.execute('insert into hot_data values(NULL, \'4399\', \'zqj\', 1, 520, 521, 522, \'2018-06-06 12:21:30\', {})'.format(spide_date))
        cursor.execute('insert into hot_data values(NULL, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (data['uid'], data['uname'], int(data['card_type']), int(data['like_cnt']), 
                    int(data['repost_cnt']), int(data['reply_cnt']), data['post_date'], str(spide_date)))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    page_num = get_hot_page_num()
    hot_datas = []
    #request_before()
    for i in range(1, page_num+1):
        page_hot_data = get_hot_datas_of_page(i)
        for data in page_hot_data:
            hot_datas.append(data)
        time.sleep(2)
    save_hot_datas(hot_datas)
