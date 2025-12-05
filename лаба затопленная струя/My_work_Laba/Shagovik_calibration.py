import matplotlib.pyplot as plt

steps = [0, 910]
distance = [0, 50]

k = 50/910

plt.figure(figsize=(8, 6))
plt.title('График калибровки шагового двигателя')
plt.plot(distance, steps, linewidth = 2)
plt.scatter(distance, steps, linewidth = 2)
plt.xlabel('Расстояние')
plt.ylabel('Шаги')
plt.grid()
plt.text(0.05, 0.95, f'K = {k:.6f} мм/шаг', 
         transform=plt.gca().transAxes, fontsize=11,
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.show()


