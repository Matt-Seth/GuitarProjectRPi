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
secondPerSlice = 1 #each frame to be FFT will be this many seconds long
dev_index = 0
Freq_Tolerance = 10 # plus or Minus 10 Hz

E_Freq = 163 #on my guitar that isn't tuned, we set it to be 
A_Freq = 100


p = pyaudio.PyAudio()

stream = p.open(format=sample_format,
            channels=channels,
            input_device_index = dev_index,
            rate=fs,
            frames_per_buffer=chunk,
            input=True)


def getAudioChunk():
    frames = []
    
    for i in range(0, int(fs / chunk * secondPerSlice)):
        data = stream.read(chunk)
        npts = len(data)
        formatstr = '%iB'% npts
        convertToFloat = unpack(formatstr, data)
        frames.extend(convertToFloat)
   
    return frames
    
def fftransform(data):
    n = int(fs*secondPerSlice)
    k = np.arange(n)
    slice_duration = n/fs
    frq = k/slice_duration
    dataFFT = np.fft.fft(data)
    maxFRQ_index = int(max_frequency*slice_duration)
    frq = frq[range(maxFRQ_index)]
    dataFFT = dataFFT[range(maxFRQ_index)]
    return (frq, dataFFT)

def get_max_frq(frq, fft):
    max_frq = 0
    max_fft = 0
    for idx in range(1,len(fft)):
        if abs(fft[idx]) > max_fft:
            max_fft = abs(fft[idx])
            max_frq = frq[idx]
    return max_frq
def getNote():
    a = getAudioChunk()
    f = fftransform(a)
    freq = get_max_frq(f[0], f[1])
    print(freq)
    if abs(freq - E_Freq):
        return 'Low E'
    if abs(freq - A_Freq):
        return 'A'