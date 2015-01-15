from scipy import misc
import numpy

import numpy as np
import time
from os import getcwd
def speedx(snd_array, factor):
    """ Speeds up / slows down a sound, by some factor. """
    indices = np.round( np.arange(0, len(snd_array), factor) )
    indices = indices[indices < len(snd_array)].astype(int)
    return snd_array[ indices ]

def stretch(snd_array, factor, window_size, h):
    """ Stretches/shortens a sound, by some factor. """
    phase  = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros( len(snd_array) /factor + window_size)

    for i in np.arange(0, len(snd_array)-(window_size+h), h*factor):

        # two potentially overlapping subarrays
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]

        # the spectra of these arrays
        s1 =  np.fft.fft(hanning_window * a1)
        s2 =  np.fft.fft(hanning_window * a2)

        #  rephase all frequencies
        phase = (phase + np.angle(s2/s1)) % 2*np.pi

        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        i2 = int(i/factor)
        result[i2 : i2 + window_size] += hanning_window*a2_rephased

    result = ((2**(16-4)) * result/result.max()) # normalize (16bit)

    return result.astype('int16')

def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)


from scipy.io import wavfile
fps, bowl_sound = wavfile.read("pianoputer/bowl.wav")

tones = range(-32,33)
transposed_sounds = [pitchshift(bowl_sound, n) for n in tones]

import pygame
import random
from time import sleep

pygame.mixer.init(frequency=fps, size=-16, buffer=128, channels=64) # so flexible ;)
screen = pygame.display.set_mode((150,150)) # for the focus

keys = open('pianoputer/typewriter.kb').read().split('\n')
sounds = map(pygame.sndarray.make_sound, transposed_sounds)
key_sound = dict( zip(keys, sounds) )
#print key_sound
is_playing = {k: False for k in keys}


in_image = misc.imread('x.png')
j = 0
numpy.set_printoptions(linewidth = 300)

for i in range(len(in_image[0,:])):
    j+=1
    col = in_image[:,i][:,0]
    for note in enumerate(col):
        sounds[note[0]].set_volume(float(note[1])/255)
        sounds[note[0]].play()
    sleep(0.1)
    for note in enumerate(col):
        sounds[note[0]].fadeout(1000)
        print ' ' + str(note[1]),
    print


for note in sounds:
    note.fadeout(1000)
