import h5py
import numpy as np
import matplotlib.pyplot as plt

inputFilePath = r"C:\Researches\Data\MPS3\202103_2\RIXS"
base = "Fe"
energyDispersion = 0.005356  # eV/subpixel
energyResolution = 0.061577  # eV
dataLength = 2000  # subpixels


def getdata(scannumber):
    global inputFilePath
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


f1 = h5py.File(inputFilePath + "\\" + "Fe_0019_d2" + ".h5", "r")

ccd1 = f1["entry"]["analysis"]["events"][()]

print(np.transpose(ccd1))

plt.hist2d(*np.transpose(ccd1), bins=[1600, 1500])

# plt.scatter(*np.transpose(ccd1), marker=".")

# plt.eventplot(np.array(ccd1))

plt.show()
