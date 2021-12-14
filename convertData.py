# %matplotlib nbagg
# import os
import h5py
import numpy as np

# import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# from scipy.optimize import curve_fit

inputFilePath = "X:\\RIXS\\Ruiz_e18603\\RIXS\\"
outputFilePath = "X:\\RIXS\\Ruiz_e18603\\ASC\\"

base = "Cu"
energyDispersion = 0.008128  # eV/subpixel

scans = np.arange(117, 280 + 1)

# os.chdir(outputFilePath)


def getdata(scannumber):
    global inputFilePath
    global outputFilePath
    global base

    if scannumber < 10:
        filename = base + "_" + "000" + str(scannumber)
    elif scannumber < 100:
        filename = base + "_" + "00" + str(scannumber)
    elif scannumber < 1000:
        filename = base + "_" + "0" + str(scannumber)
    else:
        filename = base + "_" + str(scannumber)

    f1 = h5py.File(inputFilePath + filename + "_d1.h5", "r")
    f2 = h5py.File(inputFilePath + filename + "_d2.h5", "r")
    f3 = h5py.File(inputFilePath + filename + "_d3.h5", "r")

    ccd1 = f1["entry"]["analysis"]["spectrum"][()]
    ccd2 = f2["entry"]["analysis"]["spectrum"][()]
    ccd3 = f3["entry"]["analysis"]["spectrum"][()]

    [xdata, data1] = elasticShift(ccd1)
    [_, data2] = elasticShift(ccd2)
    [_, data3] = elasticShift(ccd3)

    np.savetxt(
        outputFilePath + filename + "_d1.dat",
        np.transpose([xdata, data1]),
        delimiter="    ",
        newline="\n",
        comments="# ",
        header="ELoss, ccd1",
    )
    np.savetxt(
        outputFilePath + filename + "_d2.dat",
        np.transpose([xdata, data2]),
        delimiter="    ",
        newline="\n",
        comments="# ",
        header="ELoss, ccd2",
    )
    np.savetxt(
        outputFilePath + filename + "_d3.dat",
        np.transpose([xdata, data3]),
        delimiter="    ",
        newline="\n",
        comments="# ",
        header="ELoss, ccd3",
    )


def elasticShift(pixelData):

    global energyDispersion

    peaks, _ = find_peaks(pixelData, height=20, width=5)
    xdataPixel = np.arange(len(pixelData))

    xdataPixel = xdataPixel[(peaks[-1] - 2000) : (peaks[-1] + 200)]
    energyData = pixelData[(peaks[-1] - 2000) : (peaks[-1] + 200)]

    xDataEnergy = (xdataPixel - peaks[-1]) * energyDispersion * -1

    return [xDataEnergy, energyData]


for i, s in enumerate(scans):
    getdata(s)
