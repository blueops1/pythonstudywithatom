#! /usr/bin/env python
# coding=utf-8

__author__ = 'ryhan'

# 以下代码解决输出乱码问题
import sys
import os
import struct

# print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

# print sys.getdefaultencoding()


class WaveOps(object):
    def __init__(self):
        pass

    @staticmethod
    def add_ulaw_header(s_flie, t_file):
        """
        文件加头
        :param wavfile:
        :return:
        """

        # 文件检测
        if not s_flie or not os.path.exists(s_flie):
            return False, 's_flie not exists !'

        # 文件头
        if os.path.exists(t_file):
            with open(t_file, 'rb') as fin:
                riff_flag = fin.read(4)
                if riff_flag == 'RIFF':
                    return False, 't_file already has header with  RIFF !'
                    # riff_flag, = struct.unpack('4s', fin.read(4))

        with open(s_flie, 'rb') as fin:
            with open(t_file, 'wb') as fout:
                # fin.seek(0, os.SEEK_SET)
                start_pos = fin.tell()
                fin.seek(0, os.SEEK_END)
                end_pos = fin.tell()
                ulaw_header = WaveOps.create_ulaw_header(end_pos - start_pos)
                fout.write(ulaw_header)
                fin.seek(os.SEEK_SET)
                fout.write(fin.read())

        if not os.path.exists(t_file):
            return False, 't_file not create success !'

        with open(t_file, 'rb') as ftag:
            riff_flag = ftag.read(4)
            print riff_flag
            if riff_flag == 'RIFF':

                return True, 'add header success !'
            else:
                return False, 'add header failure ! but t_file has created ~ ! '

    @staticmethod
    def create_ulaw_header(audio_size, sampleRate=8000, bits=8, channel=1):
        """
        00H 4 char "RIFF" char riff_id[4]="RIFF"
        04H 4 long int 文件总长-8 long int size0=文总长-8
        08H 8 char "WAVEfmt " char wave_fmt[8]
        10H 4 long int 12000000H(ULAW) long int size1=0x12
        14H 2 int 07 00H int fmttag=0x07
        16H 2 int 声道数 int channel=1 或2
        18H 4 long int 采样率 long int samplespersec
        1CH 4 long int 每秒播放字节数 long int bytepersec
        20H 2 int 采样一次占字节数 int blockalign=0x01
        22H 4 long int 量化数 long int bitpersamples=8
        26H 4 char "fact" char wave_fact="fact"
        2AH 8 char 0400000000530700H定 char temp
        32H 4 char "data" char wave_data="data"
        36H 4 long int 采样数据字节数 lont int size2=文长-58
        """

        header = ''
        # 00H 4 char "RIFF" char riff_id[4]="RIFF"
        header += struct.pack('4c', 'R', 'I', 'F', 'F')
        # 04H 4 long int 文件总长-8 long int size0=文总长-8
        header += struct.pack('i', audio_size + 58 - 8)
        # 08H 8 char "WAVEfmt " char wave_fmt[8]
        header += struct.pack('8c', 'W', 'A', 'V', 'E', 'f', 'm', 't', ' ')
        # 10H 4 long int 12000000H(ULAW) long int size1=0x12
        header += '\x12\x00\x00\x00'
        # 14H 2 int 07 00H int fmttag=0x07
        header += '\x07\x00'
        # 16H 2 int 声道数 int channel=1 或2
        header += struct.pack('H', channel)
        # 18H 4 long int 采样率 long int samplespersec
        header += struct.pack('i', sampleRate)
        # 1CH 4 long int 每秒播放字节数 long int bytepersec
        header += struct.pack('i', sampleRate * bits / 8)
        # 20H 2 int 采样一次占字节数 int blockalign=0x01
        header += struct.pack('H', channel * bits / 8)
        # 22H 4 long int 量化数 long int bitpersamples=8
        header += struct.pack('i', bits)
        # 26H 4 char "fact" char wave_fact="fact"
        # rHeadInfo += struct.pack('4c', 'f', 'a', 'c', 't')
        # 2AH 8 char 0400000000530700H定 char temp
        # rHeadInfo += struct.pack('8c', 'c', 'h', 'a', 'r', 't', 'e', 'm', 'p')
        # 32H 4 char "data" char wave_data="data"
        header += struct.pack('4c', 'd', 'a', 't', 'a')
        # 36H 4 long int 采样数据字节数 lont int size2=文长-58
        header += struct.pack('i', audio_size)
        return header


if __name__ == '__main__':
    print WaveOps.add_ulaw_header('wav/test1.wav', 'wav/test2.wav')
