# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:03:44 2022

@author: Ralph Yang, Zijia Wang
"""
import os
import time

from poster import post_human_input,get_robot_output,init_chat
from recorder import start_audio

                                                
# Display and interact with the Window
# print('Chatbot->')
print('\033[32m================================================================================================\033[0m')
init_chat()
os.system('hello.mp3')
time.sleep(6)
counter = 0
while True:
    # print('Please speech after \"ON\"..........')
    # time.sleep(3)
    if counter == 0:
        print('\033[34mPlease read the following sentences loudly..........\033[0m')
        print('The goal of early calculating machines was to simplify difficult sums.\n'
              'But with the help of new technology, electronic chips replaced tubes and a revolution of artificial intelligence has arisen.\n'
              'From then on, the appearance of computers totally changed our lives. \n'
              'They can not only download information from the wet when connected by the network or mobile phone signals,\n'
              'but also solve different types of logical problems.\n')
        start_audio(time=20)
    else:
        print('\033[34mQuestion->\033[0m')
        time.sleep(2)
        start_audio(time=5)
    counter = counter + 1
    post_human_input('input.wav')
    time.sleep(1)
    idx, res = get_robot_output('response.mp3')
    # print(res)
    print('\033[34mChatbot->\033[0m\n')
    name = 'response' + str(idx) + '.mp3'
    file_s = os.stat(name)
    s_time = file_s.st_size/(1024*5)
    # print(s_time)
    os.system(name)
    time.sleep(s_time + 3)
    print('\033[32m============================================================================================\033[0m')

