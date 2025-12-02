import jetFunctions as j
import matplotlib.pyplot as plt
import time
import numpy as np 

try: 
    j.initSpiAdc()
    samples = []
    for i in range(50):
        samples.append(j.getAdc())
        time.sleep(0.1)
    data = np.array(samples)
    np.savetxt('калибровка xПа', data, fmt='%d', header='Калибровка давления 0Па', comments='', encoding='utf-8')
    plt.plot(samples)
    plt.show()
    
finally:
    j.deinitSpiAdc()