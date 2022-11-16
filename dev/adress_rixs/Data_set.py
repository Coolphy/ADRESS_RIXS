import h5py
import numpy as np

class Data_set():

    def __init__(self):
        self.data_set = {}

    def load_runNums(self, obj):
        runNums = obj.runNums
        return runNums

    def load_fileList(self, obj):
        fileList = obj.fileList
        return fileList

    def load_raw_data(self,fileName):
        file = h5py.File(fileName,'r')
        data = np.array(file["entry"]["analysis"]["spectrum"][()])
        return data

    def load(self,obj):
        runNums = self.load_runNums(obj)
        fileList = self.load_fileList(obj)

        for runNum in runNums:
            for i in range(3):
                self.data_set[runNum][i] = self.load_raw_data(fileList[runNum][i])