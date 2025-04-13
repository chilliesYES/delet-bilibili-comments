import requests
import json
import sys
import time
import pymysql
from pathlib import Path
import configparser
import shutil

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
json_r是放被回复数据的
运行前务必先更新cookies和csrf
'''
rr = Path('json_folder/json_r/');rr.mkdir(parents=True, exist_ok=True)
tt = Path('json_folder/jsont/');tt.mkdir(parents=True, exist_ok=True)
def folderclean(folder):
    path = Path(folder)
    for i in path.iterdir():
        i.unlink()

while True:
    ask0 = input('记得更新cookies\n1.处理从aicu获取的json上传数据库并执行删除\n2.获取所有被回复以及被赞的消息上传并执行删除\n3.执行删除\n4.扫描近期评论\n5.退出\n')
    if ask0 == '1':
        mode = 1
        json_to_sql.main(connect, mode)
        go_del.main(connect)
    elif ask0 == '2':
        folderclean('json_folder/json_r')
        mode = 2
        getnew.get_reply()
        getnew.get_like()
        print('收集完成')
        json_to_sql.main(connect, 2)
        json_to_sql.main(connect, 3)
        go_del.main(connect)
        print('完成删除')
    elif ask0 == '3':
        go_del.main(connect)
    elif ask0 == '4':
        folderclean('json_folder/json_r')
        num = int(input('请输入前多少个评论数量（必须20的倍数）输入0则为全部:'))/20
        getnew.get_reply(num)
        getnew.get_like(num)
        print('收集完成')
        json_to_sql.main(connect, 2)
        json_to_sql.main(connect, 3)
        cursor.execute('''select * from main1 where status = 0''')
        newpl = cursor.fetchall()
        with open('最近评论数据.txt','w', encoding='utf-8') as f:
            for i in newpl:
                f.write(' '.join(map(str, i))+'\n')
        print('请到最近评论数据查看未删除评论\n')
    elif ask0 == '5':
        sys.exit()



