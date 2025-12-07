import matplotlib.pyplot as plt

distances = [0, 10, 20, 30, 40, 50, 60, 70, 80]

Rasxod = [18, 18.81, 19.43, 19.51, 19.56, 17.31, 15.15, 13.05, 12.23]

plt.figure(figsize=(12, 8))

plt.plot(distances, Rasxod, linewidth = 2)
plt.grid()
plt.xlabel('Расстояние, мм')
plt.ylabel('Расход Q, г/с')

plt.show()