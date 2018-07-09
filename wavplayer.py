#!usr/bin/env python
#coding=utf-8

import pyaudio
import wave
import util_voice as uv
import os

#import wavaddheader as wah

#get baiduvoice
API_KEY = 'HIqxZxcEZ1bM7IhyjryHq7nI'
SECRET_KEY = '4tiKxM41oLd289ZVITViNiFc4cIZQYhx'

testv = uv.BaiduRest('11161674',API_KEY,SECRET_KEY)
isok = testv.text2audio('九九六六你们好','test2.wav')
print(isok)


#define stream chunk
chunk = 1024

#open a wav format music
f = wave.open('test2.wav',"rb")
#instantiate PyAudio
p = pyaudio.PyAudio()
#open stream
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
    channels = f.getnchannels(),
    rate = f.getframerate(),
    output = True)
#read data
data = f.readframes(chunk)

#paly stream
while data != '':
 stream.write(data)
 data = f.readframes(chunk)

#stop stream
stream.stop_stream()
stream.close()

#close PyAudio
p.terminate()
