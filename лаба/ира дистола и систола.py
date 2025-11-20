import Ира_давление as ira
import Ира_спв as spv
import matplotlib.pyplot as plt
import numpy as np

pressures, b, a = spv.butterworth_filter(ira.pressures, spv.fs, spv.cutoff_freq)

pressures_sistola = []
times_sistola = []
for i in range(len(ira.times)):
    if ira.times[i]>8 and ira.times[i]<15:
        times_sistola.append(ira.times[i])
        pressures_sistola.append(pressures[i])

near_time_sistola = []
for i in range(len(times_sistola)):
    if times_sistola[i]>9.270 and times_sistola[i]<9.425:
        near_time_sistola.append(i)
sistola = min([pressures_sistola[i] for i in near_time_sistola]) #140


pressures_distola = []
times_distola = []
for i in range(len(ira.times)):
    if ira.times[i]>18 and ira.times[i]<26:
        times_distola.append(ira.times[i])
        pressures_distola.append(pressures[i])

near_time_distola = []
for i in range(len(times_distola)):
    if times_distola[i]>21 and times_distola[i]<22:
        near_time_distola.append(i)
distola = min([pressures_distola[i] for i in near_time_distola]) #82


plt.plot(ira.times, pressures)
plt.plot([i for i in range(61)], [140 for i in range(61)], label='Систолическое давление, 140 мм.рт.ст')
plt.plot([i for i in range(61)], [82 for i in range(61)], label='Диастолическое давление, 82 мм.рт.ст')
plt.title('График давления Иры от времени')
plt.grid()
plt.xlabel('Время, с')
plt.ylabel('Давление, мм.рт.ст.')
plt.legend(loc='upper right')
plt.show()
