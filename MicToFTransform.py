import pyaudio
import wave
import time
#import thread
import numpy as np

chunk = 4096  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
max_frequeny = fs/2
secondPerChunk = 1
filename = "Chunk.wav"
dev_index = 0

p = pyaudio.PyAudio()

stream = p.open(format=sample_format,
                channels=channels,
                input_device_index = dev_index,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

def getAudioChunk():
    print("recording")
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
    print("done recording")
    return data
def fft(data):
    dataFFT = np.fft.fft(data)

a = getAudioChunk()

print(type(a))
print(a)

