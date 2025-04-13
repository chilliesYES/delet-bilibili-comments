import json
import sys
import pymysql
from pathlib import Path
import configparser

def rejson(path, mode):#处理各种json，接受单个json
    if mode ==1:#模式1处理aicu的json由于本身结构合理仅做脱掉最外层处理
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
            ea = data['data']['replies']
            return ea
    elif mode ==2:#模式2处理来自https://api.bilibili.com/x/msgfeed/reply?的json，返回对象列表
        tank1 = []#m r o t
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)#data.items
            data1 = data['data']['items']
            for i in data1:
                fa_time = int(str(i['reply_time']) + '00')#这里有点混乱反正这句必须在最上面
                i = i['item']
                #print(fa_time)
                if i['target_reply_content'] == "":
                    m = i['title'];r = i['target_id'];o = i['subject_id'];t = fa_time
                    tank1.append([m,r,o,t])
                else:
                    m = i['target_reply_content'];r = i['target_id'];o = i['subject_id'];t = fa_time
                    tank1.append([m,r,o,t])
            return tank1
    elif mode ==3:
        tank1 = []#m r t z|由于该api下没有oid数据继续向下挖不值得这里直接去掉，对于没有回复的有赞评论进行删除可能需要手动检查
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data1 = data['data']['total']['items']
            for i in data1:
                zan = i['counts']
                rpid = i['item']['item_id']
                me = i['item']['title']
                like_time = i['like_time']
                tank1.append([me,rpid,like_time,zan])
        return tank1
def upload(message, rpid, oid, t, connect, cursor, zan=None):#此处的zan键结构与数据库不同
    try:
        cursor.execute('''select max(id1) from main1''')
        id1 = cursor.fetchone()[0] + 1
        cursor.execute('''
        insert into main1(id1, message, rpid, oid, t, zan)
        values (%s,%s,%s,%s,%s,%s)
        ''', (int(id1), message, rpid, oid, t, zan))
        connect.commit()
    except Exception as e:#1062代码为唯一值冲突
        er = eval(str(e))[0]
        if er == 1062:
            pass
            #print(f'**********{e}*********')
            #sys.exit()
        else:
            print(f'sql error: {er}')
            sys.exit()
        #print(er)
def main(connect, mode):
    cursor = connect.cursor()
    if mode == 1:
        jsondir = 'json_folder/jsont/'#原始文件存储aicu
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
    elif mode == 3:
        jsondir = 'json_folder/json_z/'
        for i in Path(jsondir).iterdir():
            print(f'{i.name}正在上传')
            ea = rejson(i, mode)
            for j in ea:#m r t z
                cursor.execute('''
                select 1 from main1
                where rpid = (%s)
                ''',(j[1],))
                result = cursor.fetchone()
                if result != None:
                    cursor.execute('''
                    update main1 set zan = (%s) where rpid = (%s)
                    ''', (j[3], j[1]))
                    connect.commit()
                else:
                    upload(j[0], j[1],None,j[2], connect, cursor, j[3])#message, rpid, oid, t, connect, cursor, zan=None
if __name__ == '__main__':
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
    main(connect, 3)
