#%%
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.optimize import curve_fit
import tkinter as tk
from tkinter import filedialog

#%%
def gaussian_norm(x, mu, omega, amp, a, b):
    sig = omega / 2 / np.sqrt(2 * np.log(2))
    # norm = 1.0 / (np.sqrt(2 * np.pi) * sig)
    return amp * np.exp(-((x - mu) ** 2) / (2 * sig ** 2)) + a + b * x


# def PseudoVoigt(x, x0, dx_l, dx_g, a, eta):
#     dx_g = dx_g / 2.355
#     dx_l = dx_l / 2.0
#     return a * (
#         eta
#         * (
#             np.sqrt(np.log(2.0) / np.pi)
#             * (1.0 / dx_g)
#             * np.exp(-np.log(2.0) * (x - x0) ** 2 / dx_g ** 2)
#         )
#         + (1.0 - eta) / (np.pi * dx_l * (1.0 + (x - x0) ** 2 / dx_l ** 2))
#     )


def zeroEnergy(xUncorrEnegy, uncorrData):
    global energyResolution
    peaks, properties = signal.find_peaks(
        uncorrData,
        height=((np.max(uncorrData) / 50) if (np.max(uncorrData) / 50) > 5 else 5),
        width=3,
    )

    popt, _ = curve_fit(
        gaussian_norm,
        xUncorrEnegy[peaks[-1] - 50 : peaks[-1] + 50],
        uncorrData[peaks[-1] - 50 : peaks[-1] + 50],
        p0=[0, energyResolution / 1000, properties["peak_heights"][-1], 0, 0],
        bounds=(
            [-np.inf, 0, 0, -np.inf, -np.inf],
            [np.inf, np.inf, np.inf, np.inf, np.inf],
        ),
    )
    # print(popt)
    xCorrEnergy = xUncorrEnegy - popt[0]
    return xCorrEnergy


def xCorr(refData, uncorrData):

    corr = signal.correlate(refData, uncorrData)  # consider full pattern
    lags = signal.correlation_lags(len(refData), len(uncorrData))
    lag = lags[np.argmax(corr)]
    # uncorrData = np.roll(uncorrData, lag)

    # peaks, _ = signal.find_peaks(refData, height=3, width=3)

    # corr = signal.correlate(
    #     refData[(peaks[-1] - 50) : (peaks[-1] + 50)],
    #     uncorrData[(peaks[-1] - 50) : (peaks[-1] + 50)],
    # )  # just consider elastic peak
    # lags = signal.correlation_lags(
    #     len(refData[(peaks[-1] - 50) : (peaks[-1] + 50)]),
    #     len(uncorrData[(peaks[-1] - 50) : (peaks[-1] + 50)]),
    # )
    # lag = lags[np.argmax(corr)]
    corrData = np.roll(uncorrData, lag)

    return corrData


def elasticShift(pixel, data):

    global energyDispersion
    # global dataLength

    peaks, _ = signal.find_peaks(
        data, height=((np.max(data) / 50) if (np.max(data) / 50) > 5 else 5), width=3
    )  # height and width of the elastic peak

    xDataEnergy = (pixel - peaks[-1]) * energyDispersion / 1000 * -1

    return [xDataEnergy, data]


def getdata(fileName):

    f = h5py.File(fileName)
    ccd = f["entry"]["analysis"]["spectrum"][()]
    xdata = np.arange(len(ccd))

    return [xdata, ccd]


def combineData(fileList):

    for i, s in enumerate(fileList):
        [xData, oneData] = getdata(s)
        axs[0, 0].plot(xData, oneData)
        # axs[0, 0].set_title("Raw data")
        axs[0, 0].set_xlabel("Positon (Pixels)")
        axs[0, 0].set_ylabel("Photons (Counts)")
        if i == 0:
            [xRefData, refData] = [xData, oneData]
            sumData = oneData
        else:
            oneData = xCorr(refData, oneData)
            sumData = sumData + oneData
        axs[0, 1].plot(xRefData, oneData)
        # axs[0, 1].set_title("Shifted data")
        axs[0, 1].set_xlabel("Positon (Pixels)")
        axs[0, 1].set_ylabel("Photons (Counts)")

    aveData = sumData / len(fileList)
    axs[1, 0].plot(xRefData, aveData)
    # axs[1, 0].set_title("Combined data")
    axs[1, 0].set_xlabel("Positon (Pixels)")
    axs[1, 0].set_ylabel("Photons (Counts)")

    [energy, data] = elasticShift(xRefData, aveData)
    xdata = zeroEnergy(energy, data)

    return [xdata, data]


#%%

# dataLength = 2000  # subpixels

energyDispersion = float(input("Energy dispersion (meV/subpiexel) = "))

energyResolution = energyDispersion * 10  # meV


for i in range(1000):
    try:
        root = tk.Tk()
        root.withdraw()
        fileList = list(filedialog.askopenfilenames(title="Select ADRESS data files"))
        # print(fileList)
        if len(fileList) == 0:
            break

        fig, axs = plt.subplots(2, 2, figsize=(6.4 * 2, 4.8 * 2))

        [X, Y] = combineData(fileList)

        axs[1, 1].plot(X, Y)
        # axs[1, 1].set_title("Calibrated data")
        axs[1, 1].set_xlabel("Energy Loss (eV)")
        axs[1, 1].set_ylabel("Photons (Counts)")
        plt.show()

        f = filedialog.asksaveasfile(
            mode="w",
            filetypes=[("txt file", ".txt")],
            defaultextension=".txt",
            title="Save the spectrum as",
        )
        if f is None:
            continue

        np.savetxt(
            f,
            np.transpose([X[::-1], Y[::-1]]),
            delimiter="\t",
            newline="\n",
            comments="# ",
            header="ELoss(eV)" + "\n" + "Photons(counts)",
        )
        f.close()
    except:
        print("Broken files !")
        plt.close()
    continue
