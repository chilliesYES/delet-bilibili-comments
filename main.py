import requests
import json
import sys
import time
import pymysql
from pathlib import Path
import configparser

import getnew
import go_del
import json_to_sql

config = configparser.RawConfigParser()
config.read('config.ini')
ip = config.get('sqlserver', 'host')
user = config.get('sqlserver', 'user')
pw = config.get('sqlserver', 'password')
database = config.get('sqlserver', 'database')
connect = pymysql.connect(host=ip,
                          user=user,
                          password=pw,
                          database=database,
                          port=3306)  # 服务器名,账户,密码,数据库名
if connect:
    print("连接成功!")
    cursor = connect.cursor()
else:
    print("连接数据库失败")
    sys.exit()
'''
aicu截的json放jsont
json_t是放被回复数据的
'''

ask0 = input('1.处理从aicu获取的json上传数据库并执行删除\n2.获取被回复的消息上传并执行删除')
if ask0 == '1':
    mode = 1
    pass
if ask0 == '2':
    mode = 2
    getnew.get_reply()
    json_to_sql.main(connect, mode)
    go_del.main(connect)



