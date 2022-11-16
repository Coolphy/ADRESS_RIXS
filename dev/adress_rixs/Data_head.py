import h5py
import numpy as np

class Meta_string():

    def __init__(self,fileName) -> None:
        self.fileName = fileName

    def load(self,str):
        file = h5py.File(self.fileName,'r')
        metaData = file["entry"]["instrument"]["NDAttributes"][str][()]
        return metaData

class Data_head():

    def __init__(self):
        self.useful_strings = [
            "PhotonEnergy",
            "PolarMode",
            "SampleTemp",
            "SampleXs",
            "SampleYs",
            "SampleZ",
            "SampleTheta",
            "SamplePhi",
            "SampleTilt",
            "AcquireTime",
            "ExposureSplit",
            "ExitSlit",
            "BeamCurrent",
            ]
        self.metaDict = {}

    def load(self, fileName):

        ms = Meta_string(fileName)

        for str in self.useful_strings:
            self.metaDict[str] = np.round(ms.load(str),4)