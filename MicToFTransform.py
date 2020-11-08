import pyaudio
import wave
import time
#import thread
import numpy as np

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
max_frequeny = fs/2
secondPerSlice = 1 #each frame to be FFT will be this many seconds long
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
    frames = []
    print("recording")
    for i in range(0, int(fs / chunk * secondPerSlice)):
        data = stream.read(chunk)
        frames.append(data)
    print("done recording")
    return frames
def fftransform(data):
    n = int(fs*secondPerFrame)
    dataFFT = np.fft.fft(data)/n #F transform and normalize by dividing by the expected number of elements in the slice.



a = getAudioChunk()


wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()