import requests
import pymysql
import sys
import time
import random
from requests.adapters import HTTPAdapter
import configparser
import json


'''
执行删除操作，删除成功后修改数据库状态码
'''

def gosleep():
    ttt = random.uniform(0.3, 0.5)#这里修改暂停时间范围，如果想当快银自己去下面把函数删掉
    time.sleep(ttt)
def getfromsql(n):
    cursor.execute('''
    select oid,rpid,status from main1
    where id1=(%s)
    ''',(n,))
    connect.commit()
    result = cursor.fetchall()
    if result:
        return result
    else:
        return [[1],]
def qd(n):#确定对应id1的状态
    cursor.execute('''
        select status from main1
        where id1=(%s)
        ''', (n,))
    result = cursor.fetchall()
    #print(result)
    if result:
        return result[0][0]
    else:#id不存在返回1默认已删除
        return 1
def updatesql(o, r):
    cursor.execute(f'''
    update main1
    set status = 1
    where rpid={r}
    ''')
    connect.commit()
def de(oid, rpid):
    sess = requests.Session()#这里是配置request的地方
    sess.mount('http://', HTTPAdapter(max_retries=3))
    sess.mount('https://', HTTPAdapter(max_retries=3))
    sess.keep_alive = False  # 关闭多余连接
    yourcsrf = config.get('selfinfo', 'csrf')  # cookie里的bili_jct项
    yourcooike = config.get('selfinfo', 'cookie')
    ua = config.get('selfinfo', 'user-agent')
    headers = {
        'user-agent':ua,
    }
    cookie = {
        'cookie': yourcooike
    }
    data = {
        'csrf': yourcsrf,
        'oid': oid,
        'rpid': rpid,
        'type': '1'
    }
    url_d = 'https://api.bilibili.com/x/v2/reply/del?'
    trytime = 0
    while trytime < 4:
        try:
            re = sess.post(url_d, headers=headers, cookies=cookie, data=data, timeout=20)
            print(f"删除{re.text}   {rpid}")#正确回复{"code":0,"message":"0","ttl":1}
            try:
                rej = json.loads(re.text)
            except Exception as e:
                print(str(e)+'出现异常，请更新信息')
                sys.exit()
            return rej
        except requests.exceptions.Timeout:
            trytime += 1
            print(f'请求超时，60s后将进行第{trytime}次重启服务，请耐心等待')
            time.sleep(60)
        except requests.exceptions.RequestException as e:
            print(f"请求错误{e}")
            sys.exit()
    print('请求失败，请自行检查，建议更新csrf和cookies或等待一段时间再次启动')
    sys.exit()
def start(limi,id0=1):
    global config
    sw=1
    sw2=1
    id=id0
    while sw2:
        #q = qd(id)
        q=0
        if q == 0:
            print('-------------------------启动--------------------------')
            while sw:
                two = getfromsql(id)
                two = two[0]#由于使用fechall的缘故此时two的状态为(oid,rpid)
                if len(two) > 1:#检测two内容是否符合2位形状
                    if two[2] in [2,'2']:
                        pass
                    else:
                        res = de(two[0], two[1])
                    config['num_del']['delid'] = str(id)
                    with open('config.ini', 'w') as con:#这里写了上次执行的断点id,
                        config.write(con)
                    if res['code'] in [0,-400]:
                        updatesql(two[0], two[1])
                        id += 1
                        gosleep()
                    elif res['code'] == -400:
                        print('被限速请等待')
                        time.sleep(60)
                    elif res['code'] == -403:
                        id += 1
                        gosleep()
                    else:
                        print(f'{res} 出现异常，已退出')
                        sys.exit()
                else:
                    if id<limi:
                        id+=1
                    else:
                        sw = 0
            sw2 = 0
        else:
            id += 1
def main(connect_):
    global connect, cursor, config
    connect = connect_
    config = configparser.RawConfigParser()
    config.read('config.ini')
    if connect:
        print("连接成功!")
        cursor = connect.cursor()
    else:
        print("连接数据库失败")
        sys.exit()
    cursor.execute('''select max(id1) from main1''');fi = int(cursor.fetchone()[0])
    st = int(config.get('num_del', 'delid'))
    start(fi,  st)  #终点，起点。会从头依次搜索确定状态
    connect.close()
    cursor.close()
config = None
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
    main(connect)
