# %%
from importlib import import_module
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import correlate
from scipy.optimize import curve_fit

import tkinter as tk
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler

import os
import sys

# %%


def Gaussian_amp(x, xc, fwhm, amp):
    return amp * np.exp(-4 * np.log(2) * (x - xc)**2 / (fwhm)**2)


def elasticShift(xAxis, uncorrData):
    global refElasticPixel
    peaks, _ = find_peaks(uncorrData, height=np.max(uncorrData) / 20, width=3)
    # uncorrData = np.roll(uncorrData, refElasticPixel - peaks[-1])
    try:
        popt, pcov = curve_fit(
            Gaussian_amp,
            xAxis,
            uncorrData,
            p0=[peaks[-1], 10,
                np.max(uncorrData) / 20],
        )
        # corrData = np.roll(uncorrData, refElasticPixel - round(popt[0]))
        # corrAxis = np.array(popt[0] - round(popt[0]) + refElasticPixel - xAxis)
        corrAxis = xAxis - popt[0]
    except:
        # corrData = uncorrData
        corrAxis = xAxis - peaks[-1]
    return corrAxis, uncorrData


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
    f = h5py.File(Path + '/' + scanNumber)
    ccd = f["entry"]["analysis"]["spectrum"][()]
    acqTime = np.mean(
        f["entry"]["instrument"]["NDAttributes"]["AcquireTime"][()])

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


def getInfo(scanNumber):
    try:
        f = h5py.File(Path + '/' + scanNumber)

        PhotonEnergy = round(
            np.mean(
                f["entry"]["instrument"]["NDAttributes"]["PhotonEnergy"][()]),
            3)
        PolarMode = np.mean(
            f["entry"]["instrument"]["NDAttributes"]["PolarMode"][()])
        if PolarMode == 0:
            Polarization = "LH"
        elif PolarMode == 1:
            Polarization = "LV"
        elif PolarMode == 2:
            Polarization = "C+"
        else:
            Polarization = "C-"

        Temp = round(
            np.mean(
                f["entry"]["instrument"]["NDAttributes"]["SampleTemp"][()]), 2)

        xx = round(
            np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleXs"][()]),
            4)
        yy = round(
            np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleYs"][()]),
            4)
        zz = round(
            np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleZ"][()]),
            4)
        Tht = round(
            np.mean(
                f["entry"]["instrument"]["NDAttributes"]["SampleTheta"][()]),
            3)
        Phi = round(
            np.mean(f["entry"]["instrument"]["NDAttributes"]["SamplePhi"][()]),
            3)
        Tilt = round(
            np.mean(
                f["entry"]["instrument"]["NDAttributes"]["SampleTilt"][()]), 3)

        AcqTime = np.mean(
            f["entry"]["instrument"]["NDAttributes"]["AcquireTime"][()])
        SplitTime = np.mean(
            f["entry"]["instrument"]["NDAttributes"]["ExposureSplit"][()])
        ExitSlit = np.mean(
            f["entry"]["instrument"]["NDAttributes"]["ExitSlit"][()])
        Ring = round(
            np.mean(
                f["entry"]["instrument"]["NDAttributes"]["BeamCurrent"][()]),
            0)
        fileInfo = str("Filename: " + scanNumber + "\n" + "PhotonEnergy: " +
                       str(PhotonEnergy) + " eV\n" + "Polarization: " +
                       Polarization + "\n" + "Temp: " + str(Temp) + " K\n" +
                       "Sample X: " + str(xx) + " mm\n" + "Sample Y: " +
                       str(yy) + " mm\n" + "Sample Z: " + str(zz) + " mm\n" +
                       "Theta: " + str(Tht) + " deg.\n" + "Phi: " + str(Phi) +
                       " deg.\n" + "Tilt: " + str(Tilt) + " deg.\n" +
                       "Acquire Time: " + str(AcqTime) + " s\n" +
                       "Split Time: " + str(SplitTime) + " s\n" +
                       "Exit Slit: " + str(ExitSlit) + " um\n" +
                       "Ring Current: " + str(Ring) + " mA\n\n")
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
    # pixelData = data / totalTime * 300  # normalize to 5 minutes
    pixelData = data
    energyAxis, energyData = EnergyTrans(pixelData)

    return [energyAxis, energyData]


def readfiles():
    Path = entry1.get()
    listbox.delete(0, tk.END)
    list = sorted(os.listdir(Path))
    for file in list:
        listbox.insert(tk.END, file)
    listbox.see(tk.END)

def readfiles_enter(self):
    readfiles()

def plotdata_double(self):
    plotdata()

def plotdata():
    global Path,scans, energyDispersion, Data, headline
    Path = entry1.get()

    cname = listbox.curselection()

    if len(cname) != 0:
        scans = []
        for i in cname:
            op = listbox.get(i)
            scans.append(op)

    if var1.get() == 0:
        text1.delete('1.0', tk.END)
        plt.cla()
        Data = np.array([])
        headline = ''

    for x in scans:
        fileInfo = getInfo(x)
        text1.insert(tk.END, fileInfo)

    energyDispersion = float(entry4.get())

    [X, Y] = CombineData(scans)
    shift = float(entry3.get())

    if Data.size == 0 :
        Data = np.transpose([X + shift, Y])
        headline = entry2.get()
    else:
        Data = np.hstack((Data, np.transpose([X + shift, Y])))
        headline =  headline + '\t' + entry2.get()

    label = entry2.get()
    plt.plot(X + shift, Y, label=label)
    # axs[1, 1].set_title("Calibrated data")
    plt.xlabel("Energy Loss ( eV )")
    plt.ylabel("Counts ( arb. u. )")
    plt.legend()
    plt.draw()

def openpath():
    path = filedialog.askdirectory(title="Select data path")
    entry1.delete(0, tk.END)
    entry1.insert(tk.END,path)
    readfiles()

def savedata():
    global Data, headline
    outputfile = filedialog.asksaveasfile(mode="w",filetypes=[("txt file", ".txt")],defaultextension=".txt",title="Save the spectrum as")
    np.savetxt(outputfile, Data, delimiter='\t',header=headline, comments='# ')
    outputfile.close()



# %%
scans=[]
Data = np.array([])
headline = ''

root = tk.Tk()
root.wm_title("RIXSPlot for ADRESS")

L1 = tk.Button(root, text="RIXS data path", font=48,command=openpath)
L1.grid(row=0, column=0, columnspan=2)
entry1 = tk.Entry(root, width=60, font=48)
entry1.grid(row=0, column=2, sticky="w")

entry1.bind('<Return>', readfiles_enter)

listbox = tk.Listbox(root,
                     listvariable=[],
                     font=48,
                     height=30,
                     selectmode="extended")
listbox.grid(row=1, column=0, columnspan=2, sticky="nwes", padx=10, pady=10)

listbox.bind('<Double-1>', plotdata_double)

L4 = tk.Label(root, text="Energy Dispersion", font=48)
L4.grid(row=2, column=0)
entry4 = tk.Entry(root, width=20, font=48)
entry4.insert(tk.END, '1')
entry4.grid(row=2, column=1)

L3 = tk.Label(root, text="Shift", font=48)
L3.grid(row=3, column=0)
entry3 = tk.Entry(root, width=20, font=48)
entry3.insert(tk.END, '0')
entry3.grid(row=3, column=1)

L2 = tk.Label(root, text="Label", font=48)
L2.grid(row=4, column=0)
entry2 = tk.Entry(root, width=20, font=48)
entry2.insert(tk.END, 'Untitled')
entry2.grid(row=4, column=1)

button1 = tk.Button(master=root, text="Plot", width=10, font=48, command=plotdata)
button1.grid(row=5, column=0)

button2 = tk.Button(master=root, text="Save", width=10, font=48, command=savedata)
button2.grid(row=5, column=1)

var1 = tk.IntVar()
c1 = tk.Checkbutton(root,
                    text='hold',
                    font=48,
                    variable=var1,
                    onvalue=1,
                    offvalue=0)
c1.grid(row=0, column=4, columnspan=2)

fig = plt.figure(figsize=(4.8 * 2.5, 3.6 * 2))
refElasticPixel = 4000

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().grid(row=1,
                            column=2,
                            rowspan=6,
                            columnspan=2,
                            sticky="nwes",
                            padx=10,
                            pady=10)

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.grid(row=0, column=3, sticky="nw")
toolbar.update()
# canvas.get_tk_widget().grid(row=1, column=2, rowspan=5, columnspan=2, sticky="nwes")


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)

text1 = tk.Text(root, font=48, height=30, width=30)
text1.grid(row=1, column=4, rowspan=5,sticky="nwes", padx=10, pady=10)

# col_count, row_count = root.grid_size()
# for col in range(col_count):
#     root.grid_columnconfigure(col, minsize=120)
# for row in range(row_count):
#     root.grid_rowconfigure(row, minsize=40)

root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
tk.mainloop()