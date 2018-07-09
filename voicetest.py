#coding:utf-8
import util_voice as uv

API_KEY = 'HIqxZxcEZ1bM7IhyjryHq7nI'
SECRET_KEY = '4tiKxM41oLd289ZVITViNiFc4cIZQYhx'

testv = uv.BaiduRest('11161674',API_KEY,SECRET_KEY)
isok = testv.text2audio('九九六六你们好','test.wav')
print(isok)
