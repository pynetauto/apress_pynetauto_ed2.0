import matplotlib.pyplot as plt
import pandas as pd

device_uptime = {'R2': 6.87, 'SW1': 6.87, 'SW4': 11.23, 'r3': 5.22, 'sw2': 6.2, 'sw3': 11.65}
df = pd.DataFrame(list(device_uptime.items()),columns = ['host','uptime'])
#print(df)
df.plot(kind='bar',x='host',y='uptime')
plt.show()
