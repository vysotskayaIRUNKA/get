import mcp3021_driver as mcp
import time
import numpy as np

mcp = mcp.MCP3021(5)
start = time.time()
try: 
    voltages = []
    times = []
    while time.time()-start < 10:
        voltage = mcp.get_voltage()
        t = time.time() - start
        voltages.append(voltage)
        times.append(t)
        time.sleep(1)
    v = np.array(voltages)
    t = np.array(times)
    data = np.column_stack((t, v))
    np.savetxt('40mm.csv', data, delimiter=',', fmt='%.4f', header='Время[c], Напряжение[B]', comments='', encoding='utf-8')
finally:
    mcp.deinit()