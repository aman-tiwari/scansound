from scipy import misc
import numpy
import multiprocessing
import subprocess

in_image = misc.imread('x.png')

while True:
    this_col = in_image[:, 0]
