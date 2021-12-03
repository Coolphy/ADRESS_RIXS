import time
from numpy.core.shape_base import block
from watchdog.observers import Observer
from watchdog.events import *
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def newFile(fileDir):
    list = os.listdir(fileDir)
    list.sort(key=lambda fn: os.path.getmtime(fileDir + fn))
    print(list[-1])
    return list[-1]


def elasticShift(pixelData):
    global energyDispersion
    peaks, _ = find_peaks(pixelData, height=20, width=5)
    xdataPixel = np.arange(len(pixelData))
    xdataPixel = xdataPixel[(peaks[-1] - 2000) : (peaks[-1] + 200)]
    energyData = pixelData[(peaks[-1] - 2000) : (peaks[-1] + 200)]
    xDataEnergy = (xdataPixel - peaks[-1]) * energyDispersion * -1
    return [xDataEnergy, energyData]


def getdata(filename):
    global filePath
    f = h5py.File(filePath + filename, "r")
    ccd = f["entry"]["analysis"]["spectrum"][()]
    [xdata, data] = elasticShift(ccd)
    return [xdata, data]


def plotData(filename):
    [X, Y] = getdata(filename)
    plt.clf()
    plt.plot(X, Y, label=filename)
    plt.legend()
    plt.show(block=False)


if __name__ == "__main__":
    filePath = "C:\\Researches\\Scripts\\plotRIXS\\test\\"
    energyDispersion = 0.008128  # eV/subpixel
    observer = Observer()
    observer.schedule(plotData(newFile(filePath)), filePath, recursive=True)
    fig = plt.figure()
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
