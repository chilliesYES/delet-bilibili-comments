import requests
import json
import sys
import time
import pymysql
import configparser
'''
从回复消息的界面的api获取所有被回复的消息
核心参数是reply_time，当reply_time和id为空返回最新的20个回复json，在拿到的数据里data.cursor里包含下一个请求的参数
获取和被赞评论懒的做对我而言没必要，有空再做，如果你需要逻辑和上面应该是一样的
'''


def get_reply():
    config = configparser.ConfigParser()
    config.read('config.ini')
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
            data1 = {
                'id': idd,  # 取上一个json的data.cursor.id//////data.cursor.id
                'reply_time': tdd,  # 时间戳，从上一个json取data.cursor.time
                'platform': 'web',
                'build': 0,
                'mobi_app': 'web'
            }
            re = requests.get(api, params=data1, headers=headers, cookies=cookies)
            #print(re.status_code)
            re.encoding = 'utf-8'
            json_data = json.loads(re.text)
            idd = json_data['data']['cursor']['id']
            if int(idd) != 0:
                tdd = json_data['data']['cursor']['time']
                print(idd)
                with open(f'json_folder/json_r/new_{jname}.json', 'w+', encoding='utf-8') as f:
                    f.write(re.text)
                jname = jname + 1
                time.sleep(1)
            else:
                break
        except Exception as e:
            print(e)
            break
