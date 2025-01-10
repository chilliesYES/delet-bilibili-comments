import json
import sys
import pymysql
from pathlib import Path


def rejson(path, mode):#返回单文件长列表
    if mode ==1:
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
            ea = data['data']['replies']
            return ea
    elif mode ==2:
        tank1 = []#m r o t
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)#data.items
            data1 = data['data']['items']
            for i in data1:
                fa_time = int(str(i['reply_time']) + '00')#这里有点混乱反正这句必须在最上面
                i = i['item']
                print(fa_time)
                if i['target_reply_content'] == "":
                    m = i['title'];r = i['target_id'];o = i['subject_id'];t = fa_time
                    tank1.append([m,r,o,t])
                else:
                    m = i['target_reply_content'];r = i['target_id'];o = i['subject_id'];t = fa_time
                    tank1.append([m,r,o,t])
            return tank1
def upload(message, rpid, oid, t, connect, cursor):
    try:
        cursor.execute('''
        insert into main1(message, rpid, oid, t)
        values (%s,%s,%s,%s)
        ''', (message, rpid, oid, t))
        connect.commit()
    except Exception as e:
        print(e)
def main(connect, mode):
    cursor = connect.cursor()
    if mode == 1:
        jsondir = 'json_folder/jsont/'
        for i in Path(jsondir).iterdir():
            print(f'{i.name}正在上传')
            ea = rejson(i, mode)
            for j in ea:
                m = j['message']
                r = j['rpid']
                o = j['dyn']['oid']
                t = int(j['time'])
                upload(m, r, o, t, connect, cursor)
    elif mode == 2:
        jsondir = 'json_folder/json_r/'
        for i in Path(jsondir).iterdir():
            print(f'{i.name}正在上传')
            ea = rejson(i, mode)
            for j in ea:
                upload(j[0], j[1], j[2], j[3], connect, cursor)

