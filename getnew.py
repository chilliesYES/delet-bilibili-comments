import requests
import json
from pathlib import Path
import sys
import time
import pymysql
import configparser
'''
b站api收集并保存原始数据
从回复消息的界面的api获取所有被回复的消息
核心参数是reply_time，当reply_time和id为空返回最新的20个回复json，在拿到的数据里data.cursor里包含下一个请求的参数
'''


def get_reply(lim = 999999):
    if lim == 0:
        lim = 999999
    cfolder = Path('json_folder\json_r');cfolder.mkdir(exist_ok=True, parents=True)
    for k in cfolder.iterdir():
        k.unlink()
    config = configparser.RawConfigParser()
    config.read('config.ini')
    #print(config.get('selfinfo','user-agent'))
    api='https://api.bilibili.com/x/msgfeed/reply?'
    headers = {
    'user-agent':config.get('selfinfo','user-agent')
    }
    cookies = {
    'cookie':config.get('selfinfo', 'cookie')
    }
    idd = '';jname = 1;tdd = ''
    while True:
        try:
            if jname <= lim:
                #print('iii')
                data1 = {
                    'id': idd,  # 取上一个json的data.cursor.id//////data.cursor.id
                    'reply_time': tdd,  # 时间戳，从上一个json取data.cursor.time
                    'platform': 'web',
                    'build': 0,
                    'mobi_app': 'web'
                }
                re = requests.get(api, params=data1, headers=headers, cookies=cookies)
                #print(re)
                re.encoding = 'utf-8'
                json_data = json.loads(re.text)
                idd = json_data['data']['cursor']['id']
                if int(idd) != 0:
                    tdd = json_data['data']['cursor']['time']
                    #print(idd)
                    with open(f'json_folder/json_r/hf_{jname}.json', 'w+', encoding='utf-8') as f:
                        f.write(re.text)
                    jname = jname + 1
                    #time.sleep(0.1)
                else:
                    break
            else:
                break
        except Exception as e:
            print(e)
            break
def get_like(lim = 999999):
    if lim == 0:
        lim = 999999
    cfolder = Path('json_folder\json_z');cfolder.mkdir(exist_ok=True, parents=True)
    for k in cfolder.iterdir():
        k.unlink()
    config = configparser.RawConfigParser()
    config.read('config.ini')
    apilike = 'https://api.bilibili.com/x/msgfeed/like?'
    headers = {
    'user-agent':config.get('selfinfo','user-agent')
    }
    cookies = {
    'cookie':config.get('selfinfo', 'cookie')
    }
    id = None;like_time = None;jname = 1;sw = False

    while True:
        try:
            if sw:
                print('ed')
                break
            if jname <= lim:
                params = {
                 'id': id,
                 'like_time': like_time,
                 'platform': 'web',
                 'build': 0,
                 'mobi_app': 'web'
                }
                rs = requests.get(apilike, params=params, headers=headers, cookies=cookies, stream=True)
                #print(rs.status_code)
                rs.encoding = 'utf-8'
                json_data = json.loads(rs.text)
                cursor = json_data['data']['total']['cursor']
                id = cursor['id'];like_time = cursor['time'];sw = cursor['is_end']
                #print(like_time)
                with open(f'json_folder/json_z/zan_{jname}.json', 'w+', encoding='utf-8') as f:
                    f.write(rs.text)
                jname += 1
            else:
                break
        except Exception as e:
            print(e)
            break

if __name__ == '__main__':
    get_like(3)
