import keyboard
# import sounddevice as sd
# from scipy.io.wavfile import write
#
# fs = 44100  # Sample rate
# seconds = 5  # Duration of recording

import pyaudio
import wave
from tqdm import tqdm


def start_audio(time = 5,save_file="input.wav"):
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    RECORD_SECONDS = time  #需要录制的时间
    WAVE_OUTPUT_FILENAME = save_file	#保存的文件名

    p = pyaudio.PyAudio()	#初始化
    # print("ON")
    #
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                        frames_per_buffer=CHUNK)#创建录音文件
    frames = []
    tqdm_list = tqdm(range(0, int(RATE / CHUNK * RECORD_SECONDS)),desc='Input',colour='blue',ncols=120)

    for i in tqdm_list:
        data = stream.read(CHUNK)
        frames.append(data)

    # print("OFF")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')	#保存
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# start_audio()