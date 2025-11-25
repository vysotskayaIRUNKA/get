import matplotlib.pyplot as plt

f = open('Эмилиус.csv')
r = f.readlines()
r = r[1:]
r = [i.split(',') for i in r]
times = [float(r[i][0]) for i in range(len(r))]
voltages = [float(r[i][1]) for i in range(len(r))]

k = 0.011892017224655166
b = 0.16239994826454973

pressures = [(i-b)/k for i in voltages]

plt.plot(times, pressures)

plt.title('График давления Эмиля от времени')
plt.grid()
plt.xlabel('Время, с')
plt.ylabel('Давление, мм.рт.ст.')
plt.show()