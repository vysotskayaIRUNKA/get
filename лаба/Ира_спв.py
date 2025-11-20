import Ира_давление as ira
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
for i in range (len(ira.times)):
    if ira.times[i]>12 and ira.times[i]<13: 
        times.append(ira.times[i])
        pressures.append(ira.pressures[i])
times = np.array(times)
pressures = np.array(pressures)
detrended_pressures = signal.detrend(pressures, type='linear')
average_time_step = 0.0002
fs = 1/average_time_step
cutoff_freq = 25

filtered_signal, b, a = butterworth_filter(detrended_pressures, fs, cutoff_freq)

peak1 = []
times_peak1 = []
for i in range(len(times)):
    if times[i]>12.2 and times[i]<12.4:
        peak1.append(filtered_signal[i])
        times_peak1.append(times[i])
sistola = max(peak1)
time_sistola = [times_peak1[i] for i in range(len(peak1)) if peak1[i]==sistola]
#время высокого пика -- 12.3056

peak2 = []
times_peak2 = []
for i in range(len(times)):
    if times[i]>12.5 and times[i]<12.6:
        peak2.append(filtered_signal[i])
        times_peak2.append(times[i])
distola = max(peak2)
time_distola = [times_peak2[i] for i in range(len(peak2)) if peak2[i]==distola]
#время низкого пика -- 12.5501

RI = 1.62/(max(time_distola)-max(time_sistola)) #RI = 6.625766871165634

if __name__ == "__main__":
    plt.grid()
    plt.scatter(times, filtered_signal)
    plt.show()