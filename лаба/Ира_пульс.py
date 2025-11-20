import Ира_давление as ira
import Ира_спв as spv
import matplotlib.pyplot as plt


puls_times = []
puls_pressures = []
pressures, b, a = spv.butterworth_filter(ira.pressures, spv.fs, spv.cutoff_freq)
for i in range(len(ira.times)):
    if ira.times[i]>=12.1 and ira.times[i]<17.5:
        puls_times.append(ira.times[i])
        puls_pressures.append(pressures[i])

detrended_puls = spv.signal.detrend(puls_pressures)


times_near1peak = [i for i in range(len(puls_times)) if puls_times[i]>12.253 and puls_times[i]<13]
puls_near1peak = [detrended_puls[i] for i in times_near1peak]
puls1peak = max(puls_near1peak)
time1peak = [puls_times[i] for i in times_near1peak if detrended_puls[i]==puls1peak] #12.3034

times_near2peak = [i for i in range(len(puls_times)) if puls_times[i]>16.5 and puls_times[i]<17]
puls_near2peak = [detrended_puls[i] for i in times_near2peak]
puls2peak = max(puls_near2peak)
time2peak = [puls_times[i] for i in times_near2peak if detrended_puls[i]==puls2peak] #16.9489

#получается, на 7 пиков (6 интервалов) приходится время 16.9489-12.3034=4.6455с
#тогда на 1 интервал приходится 0.774425с
#тогда пульс примерно 77ударов/мин (60/интервал)


plt.title('Пульс Иры')
plt.plot(puls_times, detrended_puls)
plt.grid()
plt.show()