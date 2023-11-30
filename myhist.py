import numpy as np
import matplotlib.pyplot as plt

mu1, sigma1 = 115, 15
mu2, sigma2 = 80, 40
x1 = mu1 + sigma1 * np.random.randn(10000)
x2 = mu2 + sigma2 * np.random.randn(10000)
fig, ax = plt.subplots( layout='constrained')
# the histogram of the data
n, bins, patches = ax.hist(x1, 50, facecolor='C0', alpha=0.5, label='x1')
n, bins, patches = ax.hist(x2, 50, facecolor='C2', alpha=0.5, label='x2')
ax.set_xlabel('Length [cm]')
ax.set_ylabel('Entries')
ax.set_title('Gaussian distributions')
ax.text(90, 250, r'$\mu_{1}=115,\ \sigma_{1}=15$')
ax.text(50, 400, r'$\mu_{2}=80,\ \sigma_{2}=40$')
#ax.axis([55, 175, 0, 0.03])
ax.grid(True)
ax.legend(loc="upper left")

fig.savefig("rndhist.png")
