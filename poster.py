# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 15:54:44 2022

@author: 10307
"""
import requests
# import sounddevice as sd
# from scipy.io.wavfile import write
from random import randint

# 使用长连接来加速程序的运行
s = requests.Session()
# r = s.get('http://100.80.243.130:10051/download/response.mp3')

def init_chat():
    url = 'http://100.80.243.130:10051/init'
    r = s.get(url)
    print('Init..........')
    return 0


def post_human_input(file_name):
    url = 'http://100.80.243.130:10051/post'
    files = {'file': open(file_name, 'rb')}
    r = s.post(url, files=files)
    print('Send..........')
    return 0

def get_robot_output(file_name):
    url = 'http://100.80.243.130:10051/download/'+file_name
    r = s.get(url)
    id = randint(1,100)
    with open('./response'+str(id)+'.mp3','wb') as f:
        f.write(r.content)
    print('Get..........')
    return id, r


# def recorder(file_name):
#     fs = 44100
#     second = 5
#     rd = sd.rec(int(second * fs), samplerate=fs, channels=2)
#     sd.wait()
#     write('file_name.wave', fs, rd)


# recorder()

# post_human_input('input.wav')
# get_robot_output('response.mp3')