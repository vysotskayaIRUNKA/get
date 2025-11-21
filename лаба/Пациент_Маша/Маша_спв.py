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

pressures_for_1_puls = []
times_for_1_puls = []
for i in range(len(times)):
    if times[i]>=23.05 and times[i]<=23.8:
        times_for_1_puls.append(times[i])
        pressures_for_1_puls.append(filtered_signal[i])

peak1 = []
times_peak1 = []
for i in range(len(times_for_1_puls)):
    if times_for_1_puls[i]>23.15 and times_for_1_puls[i]<23.2:
        peak1.append(pressures_for_1_puls[i])
        times_peak1.append(times_for_1_puls[i])
sistola = max(peak1)
time_sistola = [times_peak1[i] for i in range(len(peak1)) if peak1[i]==sistola]
#время высокого пика -- 23.1862

peak2 = []
times_peak2 = []
for i in range(len(times_for_1_puls)):
    if times_for_1_puls[i]>23.4:
        peak2.append(pressures_for_1_puls[i])
        times_peak2.append(times_for_1_puls[i])
distola = max(peak2)
time_distola = [times_peak2[i] for i in range(len(peak2)) if peak2[i]==distola]
#время низкого пика -- 23.4302

RI = 1.63/(max(time_distola)-max(time_sistola)) #RI = 6.680327868852465

if __name__ == "__main__":
    plt.grid()
    plt.scatter(times_for_1_puls, pressures_for_1_puls)
    plt.show()