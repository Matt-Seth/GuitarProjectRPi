import pyaudio
import wave
import time
#import thread
import numpy as np
from struct import unpack

chunk = 4096  # Record in chunks of 4096 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
max_frequency = fs/2
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
        npts = len(data)
        formatstr = '%iB'% npts
        convertToFloat = unpack(formatstr, data)
        frames.extend(convertToFloat)
    print("done recording")
    return frames
    
def fftransform(data):
    n = int(fs*secondPerSlice)
    k = np.arange(n)
    slice_duration = n/fs
    frq = k/slice_duration
    print("Type of data:")
    print(type(data))
    print(type(data[0]))
    #print(data)

    dataFFT = np.fft.fft(data)
    maxFRQ_index = int(max_frequency*slice_duration)
    frq = frq[range(maxFRQ_index)]
    dataFFT = dataFFT[range(maxFRQ_index)]
    return (frq, dataFFT)


a = getAudioChunk()
f = fftransform(a)

print(type(f[0][0]))
print(len(f[0]))
print(len(f[1]))
print(type(f[1][0]))

