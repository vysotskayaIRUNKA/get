import matplotlib.pyplot as plt 
import numpy as np

f = open('40mm.csv')
r = f.readlines()
r = r[1:]
r = [i.split(',') for i in r]
times = [float(r[i][0]) for i in range(len(r))]
voltages = [float(r[i][1]) for i in range(len(r))]
plt.plot(times, voltages)
plt.title('калибровка 40мм')
plt.grid()
plt.show()