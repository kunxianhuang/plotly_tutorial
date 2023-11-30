import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,10,100)

plt.plot(x,np.sin(x),'-')
plt.plot(x,np.cos(x),'--')

#plt.show()
plt.savefig("sin_cos.png")
plt.savefig("sin_cos.jpg")
plt.savefig("sine_cos.pdf")
