import Халид_давление as kh
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
for i in range (len(kh.times)):
    if kh.times[i]>28.9 and kh.times[i]<29.3: 
        times.append(kh.times[i])
        pressures.append(kh.pressures[i])
times = np.array(times)
pressures = np.array(pressures)
detrended_pressures = signal.detrend(pressures, type='linear')
average_time_step = 0.0002
fs = 1/average_time_step
cutoff_freq = 25

filtered_signal, b, a = butterworth_filter(detrended_pressures, fs, cutoff_freq)

pressures_for_1_puls = []
times_for_1_puls = []
for i in range(len(times)):
    if times[i]>=28.9 and times[i]<=29.5:
        times_for_1_puls.append(times[i])
        pressures_for_1_puls.append(filtered_signal[i])

peak1 = []
times_peak1 = []
for i in range(len(times_for_1_puls)):
    if times_for_1_puls[i]>28.9 and times_for_1_puls[i]<29.5:
        peak1.append(pressures_for_1_puls[i])
        times_peak1.append(times_for_1_puls[i])
sistola = max(peak1)
time_sistola = [times_peak1[i] for i in range(len(peak1)) if peak1[i]==sistola]

peak2 = []
times_peak2 = []
for i in range(len(times_for_1_puls)):
    if times_for_1_puls[i]>28.9:
        peak2.append(pressures_for_1_puls[i])
        times_peak2.append(times_for_1_puls[i])
distola = max(peak2)
time_distola = [times_peak2[i] for i in range(len(peak2)) if peak2[i]==distola]
#позиция и время высокого и низкого пика - (0,226)  (-0.01513).... 29.0102 29.299
#RI = 6,16
#PerRI=(0,2679- 0,0022)0,2679 = 0,917%

if __name__ == "__main__":
    plt.grid()
    plt.scatter(times_for_1_puls, pressures_for_1_puls)
    plt.show()

    print(max(time_distola), max(time_sistola))
