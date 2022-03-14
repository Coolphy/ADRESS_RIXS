#%%
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import correlate
from scipy.signal import correlation_lags
from scipy.optimize import curve_fit

import tkinter as tk
from tkinter import filedialog
from cycler import cycler

custom_cycler = cycler(
    color=["#0072BD", "#D95319", "#EDB120", "#7E2F8E", "#77AC30", "#4DBEEE", "#A2142F"]
)
plt.rc("axes", prop_cycle=custom_cycler)

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
    peaks, properties = find_peaks(
        uncorrData,
        height=((np.max(uncorrData) / 50) if (np.max(uncorrData) / 50) > 5 else 5),
        width=3,
    )

    popt, _ = curve_fit(
        gaussian_norm,
        xUncorrEnegy[peaks[-1] - 50 : peaks[-1] + 50],
        uncorrData[peaks[-1] - 50 : peaks[-1] + 50],
        p0=[
            0,
            energyResolution / 1000,
            properties["prominences"][-1],
            0,
            0,
        ],
        bounds=(
            [-0.2, 0, 0, 0, 0],
            [
                0.2,
                np.inf,
                np.inf,
                np.inf,
                np.inf,
            ],
        ),
    )
    # print(popt)
    xCorrEnergy = xUncorrEnegy - popt[0]

    return xCorrEnergy


def xCorr(refData, uncorrData):

    corr = correlate(refData, uncorrData)  # consider full pattern
    lags = correlation_lags(len(refData), len(uncorrData))
    lag = lags[np.argmax(corr)]
    corrData = np.roll(uncorrData, lag)

    return corrData


def elasticShift(pixel, data):

    global energyDispersion
    # global dataLength

    peaks, _ = find_peaks(
        data, height=((np.max(data) / 50) if (np.max(data) / 50) > 5 else 5), width=3
    )  # height and width of the elastic peak

    axs[1, 0].plot(pixel - peaks[-1], data)
    # axs[1, 0].set_title("Combined data")
    axs[1, 0].set_xlabel("Positon (Pixels)")
    axs[1, 0].set_ylabel("Photons (Counts)")

    xDataEnergy = (pixel - peaks[-1]) * energyDispersion / 1000 * -1

    return [xDataEnergy, data]


def getdata(fileName):

    f = h5py.File(fileName)
    ccd = f["entry"]["analysis"]["spectrum"][()]
    acqTime = np.mean(f["entry"]["instrument"]["NDAttributes"]["AcquireTime"][()])
    xdata = np.arange(len(ccd))

    return [xdata, ccd], acqTime


def getInfo(filename):
    try:
        f = h5py.File(filename, "r")

        PhotonEnergy = round(
            np.mean(f["entry"]["instrument"]["NDAttributes"]["PhotonEnergy"][()]), 3
        )
        PolarMode = np.mean(f["entry"]["instrument"]["NDAttributes"]["PolarMode"][()])
        if PolarMode == 0:
            Polarization = "LH"
        elif PolarMode == 1:
            Polarization = "LV"
        elif PolarMode == 2:
            Polarization = "C+"
        else:
            Polarization = "C-"

        Temp = round(
            np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTemp"][()]), 2
        )

        xx = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleXs"][()]), 4)
        yy = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleYs"][()]), 4)
        zz = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleZ"][()]), 4)
        Tht = round(
            np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTheta"][()]), 3
        )
        Phi = round(
            np.mean(f["entry"]["instrument"]["NDAttributes"]["SamplePhi"][()]), 3
        )
        Tilt = round(
            np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTilt"][()]), 3
        )

        AcqTime = np.mean(f["entry"]["instrument"]["NDAttributes"]["AcquireTime"][()])
        SplitTime = np.mean(
            f["entry"]["instrument"]["NDAttributes"]["ExposureSplit"][()]
        )
        ExitSlit = np.mean(f["entry"]["instrument"]["NDAttributes"]["ExitSlit"][()])
        Ring = round(
            np.mean(f["entry"]["instrument"]["NDAttributes"]["BeamCurrent"][()]), 0
        )
        fileInfo = str(
            "filename: "
            + filename
            + "\n"
            + "PhotonEnergy: "
            + str(PhotonEnergy)
            + " eV\n"
            + "Polarization: "
            + Polarization
            + "\n"
            + "Temp: "
            + str(Temp)
            + " K\n"
            + "Sample X: "
            + str(xx)
            + " mm\n"
            + "Sample Y: "
            + str(yy)
            + " mm\n"
            + "Sample Z: "
            + str(zz)
            + " mm\n"
            + "Theta: "
            + str(Tht)
            + " deg.\n"
            + "Phi: "
            + str(Phi)
            + " deg.\n"
            + "Tilt: "
            + str(Tilt)
            + " deg.\n"
            + "Acquire Time: "
            + str(AcqTime)
            + " s\n"
            + "Split Time: "
            + str(SplitTime)
            + " s\n"
            + "Exit Slit: "
            + str(ExitSlit)
            + " um\n"
            + "Ring Current: "
            + str(Ring)
            + " mA\n"
            + "ELoss(eV)"
            + "\t"
            + "Photons(counts/5 mins)"
        )
    except:
        fileInfo = "Empty file !"

    return fileInfo


def combineData(fileList):

    for i, s in enumerate(fileList):
        [xData, oneData], acqTime = getdata(s)
        axs[0, 0].plot(xData, oneData)
        # axs[0, 0].set_title("Raw data")
        axs[0, 0].set_xlabel("Positon (Pixels)")
        axs[0, 0].set_ylabel("Photons (Counts)")
        if i == 0:
            [xRefData, refData] = [xData, oneData]
            sumData = oneData
            fileinfo = getInfo(s)
            totaltime = acqTime
        else:
            oneData = xCorr(refData, oneData)
            sumData = sumData + oneData
            totaltime = totaltime + acqTime
        axs[0, 1].plot(xRefData, oneData)
        # axs[0, 1].set_title("Shifted data")
        axs[0, 1].set_xlabel("Positon (Pixels)")
        axs[0, 1].set_ylabel("Photons (Counts)")
    try:
        [energy, data] = elasticShift(xRefData, sumData)
        xdata = zeroEnergy(energy, data)
        ydata = data / totaltime * 300
    except:
        xdata = energy
        ydata = data / totaltime * 300
        plt.text(
            np.min(xdata),
            np.max(ydata) * 0.8,
            "Can not find elastic peak !",
            color="red",
            fontsize=16,
        )

    axs[1, 1].plot(xdata, ydata)
    # axs[1, 1].set_title("Calibrated data")
    axs[1, 1].set_xlabel("Energy Loss (eV)")
    axs[1, 1].set_ylabel("Photons (Counts / 5 minutes)")

    return [xdata, data, fileinfo]


# %%
def getvalue():
    global energyDispersion, energyResolution
    value = entry.get()
    energyDispersion = float(value)
    energyResolution = energyDispersion * 10  # meV
    input.destroy()


input = tk.Tk()
input.title("RIXSplot")
L1 = tk.Label(input, text="Energy Dispersion (meV/subpixel)")
L1.pack()
entry = tk.Entry(input, width=40, justify="center")
entry.pack()
button = tk.Button(input, text="Start", command=getvalue).pack()
input.mainloop()

for i in range(1000):
    try:
        root = tk.Tk()
        root.withdraw()
        fileList = list(
            filedialog.askopenfilenames(
                title="Select ADRESS data files", filetypes=[("HDF5 files", "*.h5")]
            )
        )
        # print(fileList)
        if len(fileList) == 0:
            break

        fig, axs = plt.subplots(2, 2, figsize=(6.4 * 2, 4.8 * 2))

        [X, Y, info] = combineData(fileList)

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
            header=info,
        )
        f.close()
    except:
        print("Broken files !")
        plt.close()
    continue
