# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 21:02:08 2018

@author: iamhexin
"""

import requests
import pymysql
import time
import random

db = pymysql.connect(host='localhost', user='root', password='你的密码', port=3306, db='quanzhigaoshou')
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS quanzhigaoshou (' +\
      'floor int(11)  NULL, '+\
      'ctime VARCHAR(45) NULL, '+\
      'comment VARCHAR(1000) NULL, '+\
      'clike int(11) NULL, '+\
      'rcount int(11) NULL, '+\
      'userid int(11) NULL, '+\
      'username VARCHAR(55) NULL, '+\
      'usersex VARCHAR(20) NULL, '+\
      'usersign VARCHAR(255) NULL, '+\
      'userlevel int(11) NULL, '+\
      'PRIMARY KEY (floor))'
cursor.execute(sql)

keys = [
    'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
    'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3'
]


def get_json(num):
    # 获取网页静态源代码
    try:
        headers = {  
            'User-Agent':keys[random.randint(0, len(keys) - 1)],  
            'Host':'api.bilibili.com',                         
            'Referer':'https://www.bilibili.com/bangumi/play/ep103088'
            }  
        proxies = {
            'http': 'http://183.166.129.53:8080'
        }
        url = 'https://api.bilibili.com/x/v2/reply?pn='+ str(num) +'&type=1&oid=9659814&sort=0'
            
        response = requests.get(url, headers = headers,proxies=proxies)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None

def get_comment_info(page_info):  
    infos = page_info['data']['replies']
    for info in infos:  
        floor = info['floor']
        ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(info['ctime'])) 
        comment = info['content']['message']
        if len(comment) > 1000:
            comment = comment[:1000]
        clike = info['like']
        rcount = info['rcount']
        userid = info['mid']
        username = info['member']['uname']
        usersex = info['member']['sex']
        try:
            usersign = info['member']['sign']
        except:
            usersign = ""
        userlevel = info['member']['level_info']['current_level']
        try:
            cursor.execute("INSERT INTO quanzhigaoshou(floor,ctime,comment,clike,rcount,userid,username,usersex,usersign,userlevel) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" ,(floor,ctime,comment,clike,rcount,userid,username,usersex,usersign,userlevel))
            db.commit()
        except:
            continue
    return

def main():   
    for n in range(364,0,-1):  
        # 对每个网页读取JSON, 获取每页数据  
        page = get_json(n)  
        get_comment_info(page)
        print('已经抓取第{}页'.format(n))  
        time.sleep(5+random.randint(1,5))   
    cursor.close()
    db.close()
    print("抓取完成")

if __name__== "__main__":   
    main()  
    

    
    
