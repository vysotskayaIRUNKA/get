import график_калибровочки as g


voltages = [g.av40, g.av80, g.av120, g.av160, g.av200]
pressures = [40, 80, 120, 160, 200]

#х - давление
#y - напряжение

sr_xy = sum([voltages[i]*pressures[i] for i in range(5)])/5
sr_x = sum([x for x in pressures])/5
sr_y = sum([y for y in voltages])/5
srx2 = sum(x**2 for x in pressures)/5

chislit = sr_xy - sr_x*sr_y 
znam = srx2 - sr_x**2 
k = chislit/znam 
b=sr_y - k*sr_x

print(k, b)
#k = 0.011892017224655166
#b = 0.16239994826454973