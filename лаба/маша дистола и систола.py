import Маша_давление as mary
import Маша_спв as spv
import matplotlib.pyplot as plt
import numpy as np

pressures, b, a = spv.butterworth_filter(mary.pressures, spv.fs, spv.cutoff_freq)

pressures_sistola = []
times_sistola = []
for i in range(len(mary.times)):
    if mary.times[i]>8 and mary.times[i]<20:
        times_sistola.append(mary.times[i])
        pressures_sistola.append(pressures[i])

near_time_sistola = []
for i in range(len(times_sistola)):
    if times_sistola[i]>10 and times_sistola[i]<10.514:
        near_time_sistola.append(i)
sistola = min([pressures_sistola[i] for i in near_time_sistola]) #128


#pressures_cool = spv.signal.detrend(pressures) #с помощью этого парня я пыталась лучше понять, где амплитуда пульсации вдвое уменьшается
pressures_distola = []
times_distola = []
for i in range(len(mary.times)):
    if mary.times[i]>23 and mary.times[i]<26:
        times_distola.append(mary.times[i])
        pressures_distola.append(pressures[i])

near_time_distola = []
for i in range(len(times_distola)):
    if times_distola[i]>25 and times_distola[i]<25.5:
        near_time_distola.append(i)
distola = min([pressures_distola[i] for i in near_time_distola]) #71


plt.plot(mary.times, pressures)
plt.plot([i for i in range(61)], [128 for i in range(61)], label='Систолическое давление, 128 мм.рт.ст')
plt.plot([i for i in range(61)], [71 for i in range(61)], label='Дистолическое давление, 71 мм.рт.ст')
plt.title('График давления Маши от времени')
plt.grid()
plt.xlabel('Время, с')
plt.ylabel('Давление, мм.рт.ст.')
plt.legend(loc='upper right')
plt.show()