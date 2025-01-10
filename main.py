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

while True:
    ask0 = input('1.处理从aicu获取的json上传数据库并执行删除\n2.获取被回复的消息上传并执行删除\n3.创建必要文件夹\n4.退出')
    if ask0 == '1':
        mode = 1
        pass
    elif ask0 == '2':
        mode = 2
        getnew.get_reply()
        json_to_sql.main(connect, mode)
        go_del.main(connect)
    elif ask0 == '3':
        rr = Path('json_folder/json_r/');rr.mkdir(parents=True, exist_ok=True)
        tt = Path('json_folder/jsont/');tt.mkdir(parents=True, exist_ok=True)
    elif ask0 == '4':
        sys.exit()







