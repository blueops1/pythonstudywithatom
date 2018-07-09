实现思路：先用ffmpeg将其他非wav格式的音频转换为wav格式，并转换音频的声道（百度支持声道为1），采样率（值为8000），格式转换完成后，再用ffmpeg将音频切成百度
支持的时长（30秒和60秒2种，本程序用的是30秒）。

# coding: utf-8
import json
import time
import base64
from inc import rtysdb
import urllib2
import requests
import os
import uuid
from inc import db_config


class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert):
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.get_token(api_key, api_secert)
        return

    def get_token(self, api_key, api_secert):
        token_url = self.token_url % (api_key, api_secert)
        r_str = urllib2.urlopen(token_url).read()
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        return True

    # 语音合成
    def text2audio(self, text, filename):
        get_url = self.getvoice_url % (urllib2.quote(text), self.cu_id, self.token_str)
        voice_data = urllib2.urlopen(get_url).read()
        voice_fp = open(filename, 'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()
        return True

    ##语音识别
    def audio2text(self, filename):
        data = {}
        data['format'] = 'wav'
        data['rate'] = 8000
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token_str

        wav_fp = open(filename, 'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        # data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        data['speech'] = base64.b64encode(voice_data).replace('\n', '')
        # post_data = json.dumps(data)
        result = requests.post(self.upvoice_url, json=data, headers={'Content-Type': 'application/json'})
        data_result = result.json()
        if(data_result['err_msg'] == 'success.'):
            return data_result['result'][0]
        else:
            return False



def test_voice(voice_file):
    api_key = "vossGHIgEETS6IMRxBDeahv8"
    api_secert = "3c1fe6a6312f41fa21fa2c394dad5510"
    bdr = BaiduRest("0-57-7B-9F-1F-A1", api_key, api_secert)

    # 生成
    #start = time.time()
    #bdr.text2audio("你好啊", "out.wav")
    #using = time.time() - start
    #print using

    # 识别
    #start = time.time()
    result = bdr.audio2text(voice_file)
    # result = bdr.audio2text("weather.pcm")
    #using = time.time() - start
    return result

def get_master_audio(check_status='cut_status'):
    if check_status == 'cut_status':
        sql = "SELECT id,url, time_long,sharps FROM ocenter_recognition WHERE status=0"
    elif check_status == 'finished_status':
        sql = "SELECT id,url, time_long,sharps FROM ocenter_recognition WHERE finished_status=0"
    else:
        return False
    data = rtysdb.select_data(sql,'more')
    if data:
        return data
    else:
        return False


def go_recognize(master_id):
    section_path = db_config.SYS_PATH
    sql = "SELECT id,rid,url,status FROM ocenter_section WHERE rid=%d AND status=0 order by id asc limit 10" % (master_id)
    #print sql
    record = rtysdb.select_data(sql,'more')
    #print record
    if not record:
        return False
    for rec in record:
        #print section_path+'/'+rec[1]
        voice_file = section_path+'/'+rec[2]
        if not os.path.exists(voice_file):
            continue
        result = test_voice(voice_file)
        print result
        exit(0)
        if result:
            #rtysdb.update_by_pk('ocenter_section',rec[0],{'content':result,'status':1})
            sql = "update ocenter_section set content='%s', status='%d' where id=%d" % (result,1,rec[0])            #print sql
            rtysdb.do_exec_sql(sql)
            parent_content = rtysdb.select_data("SELECT id,content FROM ocenter_recognition WHERE id=%d" % (rec[1]))
            #print parent_content
            if parent_content:
                new_content = parent_content[1]+result
                update_content_sql = "update ocenter_recognition set content='%s' where id=%d" % (new_content,rec[1])
                rtysdb.do_exec_sql(update_content_sql)
        else:
            rtysdb.do_exec_sql("update ocenter_section set status='%d' where id=%d" % (result,1,rec[0]))
        time.sleep(5)
    else:
        rtysdb.do_exec_sql("UPDATE ocenter_recognition SET finished_status=1 WHERE id=%d" % (master_id))
#对百度语音识别不了的音频文件进行转换
def ffmpeg_convert():
    section_path = db_config.SYS_PATH
    #print section_path
    used_audio = get_master_audio('cut_status')
    #print used_audio
    if used_audio:
        for audio in used_audio:
            audio_path = section_path+'/'+audio[1]
            new_audio = uuid.uuid1()
            command_line = "ffmpeg -i "+audio_path +" -ar 8000 -ac 1  -f wav "+section_path+"/Uploads/Convert/convert_" + str(new_audio) +".wav";
            #print command_line
            os.popen(command_line)
            if os.path.exists(section_path+"/Uploads/Convert/convert_" + str(new_audio) +".wav"):
                convert_name = "Uploads/Convert/convert_" + str(new_audio) +".wav"
                ffmpeg_cut(convert_name,audio[3],audio[0])
                sql = "UPDATE ocenter_recognition SET status=1,convert_name='%s' where id=%d" % (convert_name,audio[0])
                rtysdb.do_exec_sql(sql)
#将大音频文件切成碎片
def ffmpeg_cut(convert_name,sharps,master_id):
    section_path = db_config.SYS_PATH
    if sharps>0:
        for i in range(0,sharps):
            timeArray = time.localtime(i*30)
            h = time.strftime("%H", timeArray)
            h = int(h) - 8
            h = "0" + str(h)
            ms = time.strftime("%M:%S",timeArray)
            start_time =  h+':'+str(ms)
            cut_name = section_path+'/'+convert_name
            db_store_name = "Uploads/Section/"+str(uuid.uuid1())+'-'+str(i+1)+".wav"
            section_name = section_path+"/"+db_store_name
            command_line = "ffmpeg.exe -i  "+cut_name+"  -vn -acodec copy -ss "+start_time+" -t 00:00:30 "+section_name
            #print command_line
            os.popen(command_line)
            data = {}
            data['rid'] = master_id
            data['url'] = db_store_name
            data['create_time'] = int(time.time())
            data['status'] = 0
            rtysdb.insert_one('ocenter_section',data)

if __name__ == "__main__":
    ffmpeg_convert()
    audio = get_master_audio('finished_status')
    if audio:
         for ad in audio:
            go_recognize(ad[0])
