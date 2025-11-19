import Маша_давление as mary
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import butter, filtfilt, freqz

def butterworth_filter(signal, fs, cutoff_freq, filter_type='low', order=4):
    """
    Фильтр Баттерворта для подавления шума квантования
    
    Parameters:
    signal - входной сигнал
    fs - частота дискретизации
    cutoff_freq - частота среза
    filter_type - 'low', 'high', 'band'
    order - порядок фильтра
    """
    nyquist = fs / 2
    normal_cutoff = cutoff_freq / nyquist
    
    # Получаем коэффициенты фильтра Баттерворта
    b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)
    
    # Применяем фильтр с нулевой фазой
    filtered_signal = filtfilt(b, a, signal)
    
    return filtered_signal, b, a

times = []
pressures = []
for i in range (len(mary.times)):
    if mary.times[i]>22 and mary.times[i]<25: 
        times.append(mary.times[i])
        pressures.append(mary.pressures[i])
times = np.array(times)
pressures = np.array(pressures)
detrended_pressures = signal.detrend(pressures, type='linear')
average_time_step = 0.0002
fs = 1/average_time_step
cutoff_freq = 25

filtered_signal, b, a = butterworth_filter(detrended_pressures, fs, cutoff_freq)

plt.grid()
plt.scatter(times, filtered_signal)
plt.show()