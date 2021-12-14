import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.optimize import curve_fit
import tkinter as tk
from tkinter import filedialog


def gaussian_norm(x, mu, gamma, amp, a, b):
    sig = gamma / 2 / np.sqrt(2 * np.log(2))
    norm = 1.0 / (np.sqrt(2 * np.pi) * sig)
    return amp * norm * np.exp(-((x - mu) ** 2) / (2 * sig ** 2)) + a + b * x


def PseudoVoigt(x, x0, dx_l, dx_g, a, eta):
    dx_g = dx_g / 2.355
    dx_l = dx_l / 2.0
    return a * (
        eta
        * (
            np.sqrt(np.log(2.0) / np.pi)
            * (1.0 / dx_g)
            * np.exp(-np.log(2.0) * (x - x0) ** 2 / dx_g ** 2)
        )
        + (1.0 - eta) / (np.pi * dx_l * (1.0 + (x - x0) ** 2 / dx_l ** 2))
    )


def zeroEnergy(xUncorrEnegy, uncorrData):
    global energyResolution
    peaks, properties = signal.find_peaks(uncorrData, height=3, width=3)

    popt, _ = curve_fit(
        gaussian_norm,
        xUncorrEnegy[peaks[-1] - 50 : peaks[-1] + 50],
        uncorrData[peaks[-1] - 50 : peaks[-1] + 50],
        p0=[0, energyResolution / 1000, properties["peak_heights"][-1], 0, 0],
    )
    # print(popt)
    xCorrEnergy = xUncorrEnegy - popt[0]
    return xCorrEnergy


def xCorr(refData, uncorrData):

    corr = signal.correlate(refData, uncorrData)  # consider full pattern
    lags = signal.correlation_lags(len(refData), len(uncorrData))
    lag = lags[np.argmax(corr)]

    corrData = np.roll(uncorrData, lag)
    return corrData


def elasticShift(pixel, data):

    global energyDispersion
    global dataLength

    peaks, _ = signal.find_peaks(
        data, height=3, width=3
    )  # height and width of the elastic peak

    pixeldata = pixel[
        (peaks[-1] - dataLength) : (peaks[-1] + 100)
    ]  # data length picked
    choosedata = data[
        (peaks[-1] - dataLength) : (peaks[-1] + 100)
    ]  # need to be changed with the zero list

    xDataEnergy = (pixeldata - peaks[-1]) * energyDispersion / 1000 * -1

    return [xDataEnergy, choosedata]


def getdata(fileName):

    f = h5py.File(fileName)
    ccd = f["entry"]["analysis"]["spectrum"][()]
    xdata = np.arange(len(ccd))

    return [xdata, ccd]


def combineData(fileList):

    for i, s in enumerate(fileList):
        [xData, oneData] = getdata(s)
        if i == 0:
            [xRefData, refData] = [xData, oneData]
            sumData = oneData
        else:
            oneData = xCorr(refData, oneData)  # xCorr(refData, uncorrData):
            sumData = sumData + oneData
    aveData = sumData / len(fileList)

    [energy, data] = elasticShift(xRefData, aveData)
    xdata = zeroEnergy(energy, data)

    return [xdata, data]


energyResolution = 30  # eV
dataLength = 2000  # subpixels

energyDispersion = float(input("Energy dispersion (meV/subpiexel) = "))
# energyResolution = float(input("Energy resolution (meV) = "))

for i in range(100):
    root = tk.Tk()
    root.withdraw()
    fileList = list(filedialog.askopenfilenames(title="Select data files"))
    # print(fileList)

    [X, Y] = combineData(fileList)

    plt.figure()
    plt.plot(X, Y)
    plt.show()

    f = filedialog.asksaveasfile(
        mode="w", filetypes=[("txt file", ".txt")], defaultextension=".txt"
    )
    if f is None:
        pass
    else:
        np.savetxt(
            f,
            np.transpose([X, Y]),
            delimiter="    ",
            newline="\n",
            comments="# ",
            header="ELoss, Counts",
        )
        f.close()
