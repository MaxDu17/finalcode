import numpy as np
import wave
import struct
import scipy.io.wavfile


CHUNK = 4096
RECORDTIME = 10


rate, data_empty = scipy.io.wavfile.read('noisereduction/blank.wav')

rate_, data_filled = scipy.io.wavfile.read('noisereduction/2seconds.wav')
print(rate_)

blank = np.fft.fft(data_empty)
full = np.fft.fft(data_filled)
carrier = full
print(blank)
print(len(full))

transformed = np.fft.ifft(carrier)
#transformed = transformed.astype('uint8')
transformed = [int(np.real(trm)) for trm in transformed]
transformed = np.array(transformed)


transformed = transformed.astype("int16")


scipy.io.wavfile.write('noisereduction/cancel.wav', rate_, transformed[:])
