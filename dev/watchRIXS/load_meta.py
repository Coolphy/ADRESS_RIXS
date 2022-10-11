import h5py

import numpy as np

path = 'C:\\Researches\\Scripts\\plotRIXS\\test\\'

name = 'Cr_0026_d1.h5'

f = h5py.File(path+name,'r')

meta_data = {}
NDAttributes = f['entry']['instrument']['NDAttributes']

# print(NDAttributes.keys())

for key in NDAttributes:
    meta_data[key] = round(np.mean(NDAttributes[key]),3)

for key in meta_data:
    print(key,' = ',meta_data[key])

useful_keys = []