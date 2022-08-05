print('Sample 1 Q scan')

# %%    command
print()

# %%
import h5py
import numpy as np

f = h5py.File(
    "D:\\Reaserch\\Data\\RIXS\\DIAMOND\\CuSb2O6\\" + "i21-244622.nxs", 'r')
# command = f['entry']['scan_command'][()]
# print(command)

manipulator = f['entry']['instrument']['manipulator']

data = f['entry']['andor']['data'][()]
print(data)
print(np.shape(data))

# %%
import matplotlib.pyplot as plt

fig,ax = plt.subplots(1)
ax.pcolorfast(data[0,:,:],cmax = 30)

# plt.imshow(data[0])

# %%
import matplotlib.pyplot as plt
plt.pcolor(data[1,:,:])

# %%
import matplotlib.pyplot as plt
plt.pcolor(data[2,:,:])