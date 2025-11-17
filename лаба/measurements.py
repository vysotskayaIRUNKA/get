import spidev
import matplotlib.pyplot as plt

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1600000

def getAdc():
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 0 | adcResponse[1]) >> 1

try:
    #f = open('measure.txt', 'w')
    samples = []
    for i in range(20000):
        samples.append(getAdc())
    #for i in samples:
    #   f.write(i + '\n')
    #f.close()
    plt.plot(samples)
    plt.show()
finally:
    spi.close()