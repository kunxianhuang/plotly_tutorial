import matplotlib.pyplot as plt

names = ['group_a', 'group_b', 'group_c']
values = [1, 10, 100]

fig,ax = plt.subplots(1,3,figsize=(9, 3))


ax[0].bar(names, values)

ax[1].scatter(names, values)

ax[2].plot(names, values)


plt.suptitle('Categorical Plotting')
plt.show()
