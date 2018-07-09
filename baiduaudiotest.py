#coding:utf-8
from aip import AipSpeech
import mp3

""" 你的 APPID AK SK """
APP_ID = '11161674'
API_KEY = 'HIqxZxcEZ1bM7IhyjryHq7nI'
SECRET_KEY = '4tiKxM41oLd289ZVITViNiFc4cIZQYhx'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result  = client.synthesis('你好百度', 'zh', 1, {
    'vol': 5,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)
print(dict)

import os
os.system('auido.mp3')
