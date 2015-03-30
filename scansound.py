import numpy as np
import scikits.audiolab as lab
from scipy import misc
from scipy.io import wavfile
import matplotlib.pyplot as plt
from instuments import piano_freqs

import sys

if len(sys.argv) != 2:
    print 'Usage: python scansound.py <image-to-scan> <audio-output-filename>'
    raise SystemExit

img_file = sys.argv[0]
audio_file = sys.argv[1]

in_image = misc.imread(img_file)
np.set_printoptions(linewidth = 300)
n_cols = len(in_image[0,:])
n_rows = len(in_image[:,0])
cols_per_sec = 4
length = n_cols/4

pi = np.pi
sample_rate = 44000
dt = 1.0/sample_rate
t = np.arange(0.0, float(n_cols)/cols_per_sec, dt)

sin_array = []

#logspace: np.logspace(np.log10(30),np.log10(20000), 64) ~ can use instead of piano freqs for weird sound
for freq in piano_freqs: 
    sin_array.append(np.sin(2*pi*freq*t))

sin_array = np.asarray(sin_array)

print 'Cols: ' + str(n_cols)
print 'Rows: ' + str(n_rows)
print 'Running time: ' + str(length) + ' seconds'
note_window = sample_rate/cols_per_sec

for i in range(n_rows):
    row = in_image[i,:][:,0]
    row = 1.0 - row/255.0
    row = np.repeat(row, note_window)
    sin_array[i] = sin_array[i] * row

summed_array = np.sum(sin_array, axis=0)
summed_array /= np.max(np.abs(summed_array),axis=0)
wavfile.write(audio_file, rate=44000, data=summed_array.astype('float32'))

plt.specgram(summed_array.astype('float32'), Fs=44000)
plt.show()
