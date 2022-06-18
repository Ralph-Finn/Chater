# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 15:47:11 2022

@author: 10307
"""


from flask import send_file, send_from_directory,Flask,request
import os
from gtts import gTTS
import speech_recognition as sr
# import chatbot
from shutil import copyfile
import time
from md5hash import scan
import subprocess
import os
from pydub import AudioSegment
import subprocess
import os
import v2id
import chat_anna
from IPython.display import Audio
import torch
import ss2
from scipy.io.wavfile import write


app = Flask(__name__)

global speaker_feature
speaker_feature = '0'
# model,config = v2id.get_model('models/stylespeech.pth')


args = dict()
args['rate'] = 19000
args['text'] = 'TTS.'
args['ref_audio'] = '/workspace/Chater/input_ref.wav'
args['save_path'] = "/workspace/Chater/output_speech.wav"
args['lexicon_path'] = './lexicon/librispeech-lexicon.txt'

model,config = ss2.get_model('./models/stylespeech.pth')


vocoder = torch.hub.load('descriptinc/melgan-neurips', 'load_melgan')
# 语音转文字
def Speech_To_Text(file_name):
    r = sr.Recognizer()
    file = sr.AudioFile(file_name)
    with file as source:
        audio = r.record(source)
    text = r.recognize_google(audio, show_all=True)
    try:
        text = text['alternative'][0]['transcript']
    except:
        text = 'Please repeat'
        print("Error in speech to text process!")
    return text

# def subprocess_run(text,sp_feature,save):
#     text = '\''+text+'\''
#     command = ["tts", "--text", text ,'--model_name','tts_models/en/vctk/vits', '--speaker_idx', sp_feature, '--out_path' ,save]
#     with open('./logfile.txt','w') as fd:
#         subprocess.run(command,shell=False,stdout = fd)
#     return 0

def Text_To_Speech(text,model,config,args,save_path):
    # ret = subprocess_run(text,speaker_feature,'/workspace/Chater/output_speech.wav')
    args['text'] = text
    mel = ss2.get_mel(model,config,args)
    mel = torch.tensor(mel,device=torch.device('cuda'))
    mel = mel.permute(0,2,1)
    audio = vocoder.inverse(mel)
    audio_numpy = audio[0].data.cpu().float().numpy()
    write("/workspace/Chater/output_speech.wav", args['rate'], audio_numpy)
    wav2mp3("/workspace/Chater/output_speech.wav",save_path) #get mp3 file
    return 0


def wav2mp3(filepath, savepath):
    sourcefile = AudioSegment.from_wav(filepath)
    filename = filepath.split('/')[-1].split('.wav')[0].replace(' ', '_') + '.mp3'
    sourcefile.export(savepath, format="mp3")
    
def check_update(old,video_file):
    while True:
        new = scan(video_file)
        if new != old:
            break
        time.sleep(1)
    time.sleep(3)
    return 0

@app.route("/init", methods=['GET'])
def initer():
    # 每次client 重启时将特征置为0
    global speaker_feature
    speaker_feature = '0'
    return 'init done'

@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    return send_from_directory('/workspace/Chater/', filename, as_attachment=True)

@app.route("/post", methods=['POST'])
def up():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    global speaker_feature
    video_file = '/workspace/Avatar_proj/4-gtm_demo/results/result_voice.mp4'
    old = scan(video_file)
    file = request.files['file']
    file.save('/workspace/Chater/input.wav')#保存文件
    # print('============Get wav!============')
    if speaker_feature == '0':
        print('Generate speaker feature........')
        time.sleep(3)
        copyfile('/workspace/Chater/input.wav', '/workspace/Chater/input_ref.wav')
        speaker_feature = '1'
        res = 'You have created your personalized chat voice!'
    else:
        text = Speech_To_Text('/workspace/Chater/input.wav')
        print('Get input--> '+text)
        res = chat_anna.chat(text)
    # 合成语音
    ret = Text_To_Speech(res,model,config,args,'/workspace/Chater/response.mp3')
    
    # Text_To_Speech_ch(res, wav_path))
    # 检测文件是否生成
    # check_update(old,video_file)
    # copyfile(video_file, '/workspace/Chater/response.mp4')
    print('Get video!')
    return res


app.run(host='0.0.0.0', port = 8802)
