import Маша_давление as mary
import Маша_спв as spv
import matplotlib.pyplot as plt


puls_times = []
puls_pressures = []
pressures, b, a = spv.butterworth_filter(mary.pressures, spv.fs, spv.cutoff_freq)
for i in range(len(mary.times)):
    if mary.times[i]>=21 and mary.times[i]<24.5:
        puls_times.append(mary.times[i])
        puls_pressures.append(pressures[i])

detrended_puls = spv.signal.detrend(puls_pressures)

times_near1peak = [i for i in range(len(puls_times)) if puls_times[i]>21 and puls_times[i]<21.4]
puls_near1peak = [puls_pressures[i] for i in times_near1peak]
puls1peak = max(puls_near1peak)
time1peak = [puls_times[i] for i in times_near1peak if puls_pressures[i]==puls1peak] #21.0711

times_near2peak = [i for i in range(len(puls_times)) if puls_times[i]>23.75 and puls_times[i]<24]
puls_near2peak = [puls_pressures[i] for i in times_near2peak]
puls2peak = max(puls_near2peak)
time2peak = [puls_times[i] for i in times_near2peak if puls_pressures[i]==puls2peak] #23.8768

#получается, на 5 пиков (4 интервала) приходится время 23.8768-21.0711=2.8057с
#тогда на 1 интервал приходится 0.701425с
#тогда пульс примерно 85ударов/мин (60/интервал)


plt.title('Пульс Маши')
plt.plot(puls_times, detrended_puls)
plt.grid()
plt.show()