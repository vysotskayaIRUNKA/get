import matplotlib.pyplot as plt

m200 = open('200mm.csv')
m160 = open('160mm.csv')
m120 = open('120mm.csv')
m80 = open('80mm.csv')
m40 = open('40mm.csv')
r200_ = m200.readlines()
r200 = [r200_[i].split(',') for i in range(1, len(r200_))]
r160_ = m160.readlines()
r160 = [r160_[i].split(',') for i in range(1, len(r160_))]
r120_ = m120.readlines()
r120 = [r120_[i].split(',') for i in range(1, len(r120_))]
r80_ = m80.readlines()
r80 = [r80_[i].split(',') for i in range(1, len(r80_))]
r40_ = m40.readlines()
r40 = [r40_[i].split(',') for i in range(1, len(r40_))]
v200 = [float(r200[i][1]) for i in range(1, len(r200))]
v160 = [float(r160[i][1]) for i in range(1, len(r160))]
v120 = [float(r120[i][1]) for i in range(1, len(r120))]
v80 = [float(r80[i][1]) for i in range(1, len(r80))]
v40 = [float(r40[i][1]) for i in range(1, len(r40))]
av200 = sum(v200)/(len(r200)-1)
av160 = sum(v160)/(len(r160)-1)
av120 = sum(v120)/(len(r120)-1)
av80 = sum(v80)/(len(r80)-1)
av40 = sum(v40)/(len(r40)-1)

plt.plot([40, 80, 120, 160, 200], [av40, av80, av120, av160, av200])
plt.xlabel('Давление, мм.рт.ст.')
plt.ylabel('Напряжение, В')
plt.grid()
plt.title('График калибровки')
plt.show()