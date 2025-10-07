import numpy as nmp
import time

def get_sin_wave_amplitude(freq, time):
    s = nmp.sin(2*3.14*freq*time)
    s+=1
    s = s/2
    return s

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)