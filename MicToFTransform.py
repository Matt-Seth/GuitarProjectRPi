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
dev_index = 0 #the device index needs to be determined using the 
Freq_Tolerance = 20 # plus or Minus 10 Hz

E_Freq = 163 #on my guitar that isn't tuned, we set it to be 
A_Freq = 100

def mic_init():
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
            channels=channels,
            input_device_index = dev_index,
            rate=fs,
            frames_per_buffer=chunk,
            input=True)
    stream.stop_stream()
    return stream
def mic_deit(stream):
    stream.close()

def getAudioChunk(stream):
    frames = []
    stream.start_stream() #the start and stop stream allows the mic to stop recording so the stream doesn't overflow with bytes.
    for i in range(0, int(fs / chunk * secondPerSlice)): 
    #this for-loop gets about a second worth of data from the Mic, and converts the data to floats in a way that the FFT algorithm can manipulate
    #The reason it is a for loop and not a time dependant loop: is because of how the stream is structured, if the same quantity of data isn't
    #pulled every time, the stream throws an overflow error. 
        data = stream.read(chunk)
        npts = len(data)
        formatstr = '%iB'% npts
        convertToFloat = unpack(formatstr, data) #unpacks the bytestream to floats.
        frames.extend(convertToFloat) #the frames array stores each chunk as an 
    stream.stop_stream()
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
def getNote(stream):
    a = getAudioChunk(stream)
    f = fftransform(a)
    freq = get_max_frq(f[0], f[1])
    print(freq)
    if abs(freq - E_Freq) < Freq_Tolerance:
        return 'Low E'
    if abs(freq - A_Freq) < Freq_Tolerance:
        return 'A'