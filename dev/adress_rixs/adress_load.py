from imp import load_module
import h5py
import numpy as np

class adress_load():

    def __init__(self,fileName):
        self.file = h5py.File(fileName,'r')
        self.ccd = self.load_data(self)
        self.meta = self.load_meta(self)

    def load_data(self):
        ccd = self.file["entry"]["analysis"]["spectrum"][()]
        return ccd

    def load_meta(self):
        meta = {}
        NDAttributes = self.file['entry']['instrument']['NDAttributes']
        for key in NDAttributes:
            meta[key] = round(np.mean(NDAttributes[key]),3)
        return meta