import matplotlib.pyplot as plt

#f = open('Потылицын.csv')
#f = open('Халидикс.csv')
#f = open('Машенька.csv')
#f = open('Эмилиус.csv')
f = open('Иришка.csv')
r = f.readlines()
r = r[1:]
r = [i.split(',') for i in r]
times = [float(r[i][0]) for i in range(len(r))]
voltages = [float(r[i][1]) for i in range(len(r))]
plt.plot(times, voltages)
#plt.title('График давления от времени И.Ю.Потылицына')
#plt.title('График давления от времени Халида')
#plt.title('График давления от времени Эмиля')
plt.title('График давления от времени Иры')
plt.grid()
plt.xlabel('Время, с')
plt.ylabel('Напряжение, считываемое с помощью АЦП')
plt.show()