import pyaudio
import wave
import time
#import thread
import numpy as np
import struct

chunk = 4096  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
max_frequeny = fs/2
secondPerSlice = 3 #each frame to be FFT will be this many seconds long
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
    n = int(fs*secondPerSlice)
    k = np.arange(n)
    slice_duration = n/fs
    frq = k/slice_duration
    dataFloat = struct.unpack("%ih" % (len(data)* channels), (b''.join(data))


    dataFFT = np.fft.fft(dataFloat)/n #F transform and normalize by dividing by the expected number of elements in the slice.
    maxFRQ_index = int(max_frequency*slice_duration)
    frq = frq[range(maxFRQ_index)]
    dataFFT = dataFFT[range(maxFRQ_index)]
    return (frq, dataFFT)


a = getAudioChunk()
f = fftransform(a)

print(f[1])
print(f[2])

