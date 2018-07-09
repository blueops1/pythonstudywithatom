#coding:utf-8
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '11161674'
API_KEY = '5wK4aYucyGoLvaeCzIudGfTp'
SECRET_KEY = 'c98cd25219136ce08969f10aecc63a20'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result  = client.synthesis('你好百度', 'zh', 1, {
    'vol': 5,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)
print(dict)
