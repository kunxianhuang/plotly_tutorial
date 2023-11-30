import numpy as np
import matplotlib.pyplot as plt

amp,sigma = 100,20

x = np.linspace(0,10,50)
y = amp*np.sin(x) + 1.2*amp + sigma*np.random.randn(50)

dy = np.sqrt(y)

fig,ax = plt.subplots()

ax.errorbar(x,y,yerr=dy,fmt='o',color='black',ecolor='lightgray',elinewidth=3,capsize=0)

plt.show()
