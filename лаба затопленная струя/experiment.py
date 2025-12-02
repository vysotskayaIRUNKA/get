import jetFunctions as j
import matplotlib.pyplot as plt
import time
import numpy as np 



try: 
    j.initSpiAdc()
    j.initStepMotorGpio()
    samples = []
    step = 10
    path = 0
    while (path<=910):
        help = []
        for i in range(10):
            help.append(j.getAdc())
            time.sleep(0.1)
        samples.append(sum(help)/len(help))
        print(sum(help)/len(help))
        path+=step 
        j.stepBackward(step)
    data = np.array(samples)
    np.savetxt('80mm', data, fmt='%d', header='Измерения 80mm\nШаг мотора 10', comments='', encoding='utf-8')
    plt.plot(samples)
    plt.show()
    
finally:
    j.deinitSpiAdc()
    j.deinitStepMotorGpio()