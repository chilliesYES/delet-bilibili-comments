import requests
import pymysql
import sys
import time
import random
from requests.adapters import HTTPAdapter
import configparser

'''
执行删除操作，删除成功后修改数据库状态码
'''

def gosleep():
    ttt = random.uniform(1, 2)#这里修改暂停时间范围，如果想当快银自己去下面把函数删掉
    time.sleep(ttt)
def getfromsql(n):
    cursor.execute('''
    select oid,rpid from main1
    where id=(%s)
    ''',(n,))
    connect.commit()
    result = cursor.fetchall()
    if result:
        return result
    else:
        return [[1],]
def qd(n):
    cursor.execute('''
        select statu from main1
        where id=(%s)
        ''', (n,))
    result = cursor.fetchall()
    print(result)
    if result:
        return result[0][0]
    else:
        return 1
def updatesql(o, r):
    cursor.execute(f'''
    update main1
    set statu = 1
    where oid={o} and rpid={r}
    ''')
    connect.commit()
def de(oid, rpid):
    sess = requests.Session()
    sess.mount('http://', HTTPAdapter(max_retries=3))
    sess.mount('https://', HTTPAdapter(max_retries=3))
    sess.keep_alive = False  # 关闭多余连接

    config = configparser.RawConfigParser()
    config.read('config.ini')
    yourcsrf = config.get('selfinfo', 'yourcsrf')  # cookie里的bili_jct项
    yourcooike = config.get('selfinfo', 'yourcooike')

    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
    }
    cookie = {
        'cookie': yourcooike}
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
            print(f"{re.status_code}   {oid}")
            return int(re.status_code)
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
    sw=1
    sw2=1
    id=id0
    while sw2:
        q = qd(id)
        if q == 0:
            print('-------------------------启动--------------------------')
            while sw:
                two = getfromsql(id)
                two = two[0]
                if len(two) > 1:
                    res = de(two[0], two[1])
                    with open('his.txt', 'w') as his:#这里写了上次执行的断电id可以填到start的第二个参数
                        his.write(str(id))
                    if res == 200:
                        updatesql(two[0], two[1])
                        id += 1
                        gosleep()
                    else:
                        print(f'状态码{res}异常，已退出')
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
    global connect, cursor
    connect = connect_
    if connect:
        print("连接成功!")
        cursor = connect.cursor()
    else:
        print("连接数据库失败")
        sys.exit()
    start(9999,1)  #终点，起点，
    connect.close()
    cursor.close()
if __name__ == '__main__':
    connect = pymysql.connect(host='ip',
                              user='mycomment',
                              password='pw',
                              database='mycomment',
                              port=3306)  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
        cursor = connect.cursor()
    else:
        print("连接数据库失败")
        sys.exit()
    main(connect)