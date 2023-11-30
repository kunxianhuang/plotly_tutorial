import numpy as np
import matplotlib.pyplot as plt

data1 = np.random.rand(100)
data2 = np.random.uniform(-1,1,100)
data3 = np.random.normal(0,3.0,100)

fig, ax = plt.subplots(figsize=(5, 2.7))
ax.plot(np.arange(len(data1)), data1, label='data1')
ax.plot(np.arange(len(data2)), data2, label='data2')
ax.plot(np.arange(len(data3)), data3, 'd', label='data3')
ax.legend()
fig.savefig("random.png")
