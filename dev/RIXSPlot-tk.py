# %%
from importlib import import_module
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import correlate
from scipy.optimize import curve_fit

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler

# import os


# %%
def MakeFileName(scanNumber):
    global Atom
    if scanNumber < 10:
        fileName = "_" + "000" + str(scanNumber)
    elif scanNumber < 100:
        fileName = "_" + "00" + str(scanNumber)
    elif scanNumber < 1000:
        fileName = "_" + "0" + str(scanNumber)
    else:
        fileName = "_" + str(scanNumber)
    return fileName


def Gaussian_amp(x, xc, fwhm, amp):
    return amp * np.exp(-4 * np.log(2) * (x - xc) ** 2 / (fwhm) ** 2)


def elasticShift(xAxis, uncorrData):
    global refElasticPixel
    peaks, _ = find_peaks(uncorrData, height=np.max(uncorrData) / 20, width=3)
    uncorrData = np.roll(uncorrData, refElasticPixel - peaks[-1])
    try:
        popt, pcov = curve_fit(
            Gaussian_amp,
            xAxis,
            uncorrData,
            p0=[refElasticPixel, 10, np.max(uncorrData) / 20],
        )
        corrData = np.roll(uncorrData, refElasticPixel - round(popt[0]))
        corrAxis = np.array(popt[0] - round(popt[0]) + refElasticPixel - xAxis)
    except:
        corrData = uncorrData
        corrAxis = xAxis
    return corrAxis, corrData


def xCorr(refData, uncorrData):
    corr = correlate(refData, uncorrData)  # consider full pattern
    lag = np.argmax(corr)

    # elastic corr
    # uncorrData = np.roll(uncorrData, lag)
    # peaks, _ = find_peaks(refData, height=np.max(refData) / 20, width=3)
    # corr = correlate(
    #     refData[peaks[-1] - 50 : peaks[-1] + 50],
    #     uncorrData[peaks[-1] - 50 : peaks[-1] + 50],
    # )
    # lag = np.argmax(corr)

    corrData = np.roll(uncorrData, lag)
    return corrData


def EnergyTrans(rawData):
    global energyDispersion
    pixel = np.arange(len(rawData))
    pixelAxis, pixelData = elasticShift(pixel, rawData)
    energyAxis = np.array(pixelAxis * energyDispersion)
    return energyAxis, pixelData


def GetData(scanNumber):
    global Path
    f1 = h5py.File(Path + MakeFileName(scanNumber) + "_d1.h5", "r")
    f2 = h5py.File(Path + MakeFileName(scanNumber) + "_d2.h5", "r")
    f3 = h5py.File(Path + MakeFileName(scanNumber) + "_d3.h5", "r")
    ccd1 = f1["entry"]["analysis"]["spectrum"][()]
    ccd2 = f2["entry"]["analysis"]["spectrum"][()]
    ccd3 = f3["entry"]["analysis"]["spectrum"][()]
    acqTime1 = np.mean(f1["entry"]["instrument"]["NDAttributes"]["AcquireTime"][()])
    acqTime2 = np.mean(f2["entry"]["instrument"]["NDAttributes"]["AcquireTime"][()])
    acqTime3 = np.mean(f3["entry"]["instrument"]["NDAttributes"]["AcquireTime"][()])
    ccd = (xCorr(ccd2, ccd1) + ccd2 + xCorr(ccd2, ccd3)) / 3
    acqTime = (acqTime1 + acqTime2 + acqTime3) / 3
    return ccd, acqTime


def CombineData(scans):
    refData, totalTime = GetData(scans[0])
    data = refData
    for x in scans[1:]:
        tempData, oneTime = GetData(x)
        data = data + xCorr(refData, tempData)
        totalTime = totalTime + oneTime
    pixelData = data / totalTime * 300  # normalize to 5 minutes
    energyAxis, energyData = EnergyTrans(pixelData)
    return [energyAxis, energyData]


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


def CombineData(scans):
    refData, totalTime = GetData(scans[0])
    data = refData
    for x in scans[1:]:
        tempData, oneTime = GetData(x)
        data = data + xCorr(refData, tempData)
        totalTime = totalTime + oneTime
    pixelData = data / totalTime * 300  # normalize to 5 minutes
    energyAxis, energyData = EnergyTrans(pixelData)

    return [energyAxis, energyData]


def plot():
    global Path, start, stop, energyDispersion
    Path = entry1.get()

    # for file in os.listdir(Path):
    #     listbox.insert(0, file)

    start = int(entry2.get())
    stop = int(entry3.get())
    scans = [start + x for x in range(stop - start + 1)]
    energyDispersion = float(entry4.get())
    plt.cla()
    [X, Y] = CombineData(scans)
    plt.plot(X, Y)
    # axs[1, 1].set_title("Calibrated data")
    plt.xlabel("Energy Loss (eV)")
    plt.ylabel("Photons (Counts / 5 minutes)")
    plt.draw()


# %%
root = tk.Tk()
root.wm_title("RIXSPlot in Tk")

L1 = tk.Label(root, text="RIXS data path", font=48)
L1.grid(row=0, column=0, columnspan=2)
entry1 = tk.Entry(root, width=60, font=48)
entry1.grid(row=0, column=2, sticky="w")

listbox = tk.Listbox(root, listvariable=[], height=45, selectmode="extended")
listbox.grid(row=1, column=0, columnspan=2, sticky="nwes", padx=10, pady=10)

L2 = tk.Label(root, text="Start", font=48)
L2.grid(row=2, column=0)
entry2 = tk.Entry(root, width=10, font=48)
entry2.grid(row=2, column=1)
L3 = tk.Label(root, text="End", font=48)
L3.grid(row=3, column=0)
entry3 = tk.Entry(root, width=10, font=48)
entry3.grid(row=3, column=1)

L4 = tk.Label(root, text="Energy Dispersion", font=48)
L4.grid(row=4, column=0)
entry4 = tk.Entry(root, width=10, font=48)
entry4.grid(row=4, column=1)

button = tk.Button(master=root, text="Plot", width=10, font=48, command=plot)
button.grid(row=5, column=0, columnspan=2)

fig = plt.figure(figsize=(4.8 * 2, 3.6 * 2))
refElasticPixel = 4000

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().grid(
    row=1, column=2, rowspan=5, columnspan=2, sticky="nwes", padx=10, pady=10
)

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.grid(row=0, column=3, sticky="nw")
toolbar.update()
# canvas.get_tk_widget().grid(row=1, column=2, rowspan=5, columnspan=2, sticky="nwes")


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)

# col_count, row_count = root.grid_size()
# for col in range(col_count):
#     root.grid_columnconfigure(col, minsize=120)
# for row in range(row_count):
#     root.grid_rowconfigure(row, minsize=40)

tk.mainloop()
