# %%
from cProfile import label
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate
from scipy.optimize import curve_fit

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler

import sys
import os


# %%
def MakeFileName(scanNumber):
    global Atom
    if scanNumber < 10:
        fileName = Atom + "_000" + str(scanNumber)
    elif scanNumber < 100:
        fileName = Atom + "_00" + str(scanNumber)
    elif scanNumber < 1000:
        fileName = Atom + "_0" + str(scanNumber)
    else:
        fileName = Atom + "_" + str(scanNumber)
    return fileName


def Gaussian_amp(x, xc, fwhm, amp, y0):
    return amp * np.exp(-4 * np.log(2) * (x - xc) ** 2 / (fwhm) ** 2) + y0


def poly2(x, p0, p1, p2):
    return p0 * x ** 2 + p1 * x + p2


def poly1(x, p0, p1):
    return p0 * x + p1


def curventureFit(xdata, ydata):
    popt, _ = curve_fit(poly1, xdata, ydata)
    xdata1 = xdata[
        ((poly1(816, *popt) - 200) < ydata) & (ydata < (poly1(816, *popt) + 200))
    ]
    ydata1 = ydata[
        ((poly1(816, *popt) - 200) < ydata) & (ydata < (poly1(816, *popt) + 200))
    ]
    popt, _ = curve_fit(poly1, xdata1, ydata1)
    xdata2 = xdata[
        ((poly1(816, *popt) - 100) < ydata) & (ydata < (poly1(816, *popt) + 100))
    ]
    ydata2 = ydata[
        ((poly1(816, *popt) - 100) < ydata) & (ydata < (poly1(816, *popt) + 100))
    ]
    popt, _ = curve_fit(poly2, xdata2, ydata2)

    xdata3 = xdata[
        ((poly2(xdata, *popt) - 50) < ydata) & (ydata < (poly2(xdata, *popt) + 50))
    ]
    ydata3 = ydata[
        ((poly2(xdata, *popt) - 50) < ydata) & (ydata < (poly2(xdata, *popt) + 50))
    ]
    popt, _ = curve_fit(poly2, xdata3, ydata3)

    xdata4 = xdata[
        ((poly2(xdata, *popt) - 30) < ydata) & (ydata < (poly2(xdata, *popt) + 30))
    ]
    ydata4 = ydata[
        ((poly2(xdata, *popt) - 30) < ydata) & (ydata < (poly2(xdata, *popt) + 30))
    ]
    popt, _ = curve_fit(poly2, xdata4, ydata4)

    xdata5 = xdata[
        ((poly2(xdata, *popt) - 20) < ydata) & (ydata < (poly2(xdata, *popt) + 20))
    ]
    ydata5 = ydata[
        ((poly2(xdata, *popt) - 20) < ydata) & (ydata < (poly2(xdata, *popt) + 20))
    ]
    popt, _ = curve_fit(poly2, xdata5, ydata5)

    print(popt)
    return popt


def curventureSubtract(ccd, popt):
    data = ccd
    data[:, 1] = ccd[:, 1] - poly2(ccd[:, 0], *popt) + poly2(816, *popt)
    return data


def peakFit(ydata):
    center = np.argmax(ydata)
    xdata = np.arange(len(ydata))
    popt, _ = curve_fit(
        Gaussian_amp,
        xdata[(np.argmax(ydata) - 100) : (np.argmax(ydata) + 100)],
        ydata[(np.argmax(ydata) - 100) : (np.argmax(ydata) + 100)],
        p0=[center, 3.0, np.max(ydata), 0],
    )
    print(popt)
    return popt


def xCorr(refData, uncorrData):
    corr = correlate(refData, uncorrData)  # consider full pattern
    lag = np.argmax(corr)
    corrData = np.roll(uncorrData, lag)
    return corrData


def GetData(scanNumber):
    global Path
    f1 = h5py.File(Path + "/" + MakeFileName(scanNumber) + "_d1.h5", "r")
    f2 = h5py.File(Path + "/" + MakeFileName(scanNumber) + "_d2.h5", "r")
    f3 = h5py.File(Path + "/" + MakeFileName(scanNumber) + "_d3.h5", "r")
    ccd1 = f1["entry"]["analysis"]["events"][()]
    ccd2 = f2["entry"]["analysis"]["events"][()]
    ccd3 = f3["entry"]["analysis"]["events"][()]

    return ccd1, ccd2, ccd3


def plot():
    global Path, Atom, Scan
    Path = entry1.get()

    listbox.delete(0, tk.END)
    list = sorted(os.listdir(Path))
    for file in list:
        listbox.insert(tk.END, file)

    Atom = entry2.get()
    Scan = int(entry3.get())
    DataLength = int(entry4.get())

    plt.clf()

    ccd1, ccd2, ccd3 = GetData(Scan)

    fig.add_subplot(231).scatter(*np.transpose(ccd1), s=0.2)
    fig.add_subplot(232).scatter(*np.transpose(ccd2), s=0.2)
    fig.add_subplot(233).scatter(*np.transpose(ccd3), s=0.2)

    text1.delete("1.0", tk.END)

    p1 = curventureFit(*np.transpose(ccd1))
    p2 = curventureFit(*np.transpose(ccd2))
    p3 = curventureFit(*np.transpose(ccd3))

    text1.insert(
        tk.END,
        format(p1[0], ".3e")
        + " x^2\n"
        + format(p1[1], ".3e")
        + " x\n"
        + format(p1[2], ".3e")
        + "\n",
    )
    text1.insert(
        tk.END,
        format(p2[0], ".3e")
        + " x^2\n"
        + format(p2[1], ".3e")
        + " x\n"
        + format(p2[2], ".3e")
        + "\n",
    )
    text1.insert(
        tk.END,
        format(p3[0], ".3e")
        + " x^2\n"
        + format(p3[1], ".3e")
        + " x\n"
        + format(p3[2], ".3e")
        + "\n",
    )

    xAxis = np.arange(1632)
    plt.subplot(231).plot(xAxis, poly2(xAxis, *p1), c="r")
    plt.subplot(232).plot(xAxis, poly2(xAxis, *p2), c="r")
    plt.subplot(233).plot(xAxis, poly2(xAxis, *p3), c="r")

    ccd1 = curventureSubtract(ccd1, p1)
    ccd2 = curventureSubtract(ccd2, p2)
    ccd3 = curventureSubtract(ccd3, p3)

    # fig.add_subplot(234).scatter(*np.transpose(ccd1), s=0.2)
    # fig.add_subplot(235).scatter(*np.transpose(ccd2), s=0.2)
    # fig.add_subplot(236).scatter(*np.transpose(ccd3), s=0.2)

    line1, _, _ = np.histogram2d(*np.transpose(ccd1), bins=[1, DataLength * 4])
    line2, _, _ = np.histogram2d(*np.transpose(ccd2), bins=[1, DataLength * 4])
    line3, _, _ = np.histogram2d(*np.transpose(ccd3), bins=[1, DataLength * 4])

    xPixel = np.arange(DataLength * 4)
    fig.add_subplot(234).scatter(xPixel, *line1, s=0.5)
    fig.add_subplot(235).scatter(xPixel, *line2, s=0.5)
    fig.add_subplot(236).scatter(xPixel, *line3, s=0.5)

    fit1 = peakFit(np.array(*line1))
    fit2 = peakFit(np.array(*line2))
    fit3 = peakFit(np.array(*line3))

    text1.insert(
        tk.END,
        "xc = "
        + format(fit1[0], ".3f")
        + "\n"
        + "fwhm = "
        + format(fit1[1], ".3f")
        + "\n"
        + "Amp = "
        + format(fit1[2], ".3f")
        + "\n",
    )
    text1.insert(
        tk.END,
        "xc = "
        + format(fit2[0], ".3f")
        + "\n"
        + "fwhm = "
        + format(fit2[1], ".3f")
        + "\n"
        + "Amp = "
        + format(fit2[2], ".3f")
        + "\n",
    )
    text1.insert(
        tk.END,
        "xc = "
        + format(fit3[0], ".3f")
        + "\n"
        + "fwhm = "
        + format(fit3[1], ".3f")
        + "\n"
        + "Amp = "
        + format(fit3[2], ".3f")
        + "\n",
    )

    plt.subplot(234).plot(xPixel, Gaussian_amp(xPixel, *fit1), c="r")
    plt.subplot(235).plot(xPixel, Gaussian_amp(xPixel, *fit2), c="r")
    plt.subplot(236).plot(xPixel, Gaussian_amp(xPixel, *fit3), c="r")

    plt.draw()


# %%
root = tk.Tk()
root.wm_title("RIXSPlot in Tk")

L1 = tk.Label(root, text="RIXS data path", font=48)
L1.grid(row=0, column=0, columnspan=2)
entry1 = tk.Entry(root, width=60, font=48)
entry1.grid(row=0, column=2, sticky="w")

listbox = tk.Listbox(
    root, listvariable=[], height=20, width=20, font=36, selectmode="extended"
)
listbox.grid(row=1, column=0, columnspan=2, sticky="nwes", padx=10, pady=10)

L2 = tk.Label(root, text="Atom", font=48)
L2.grid(row=2, column=0)
entry2 = tk.Entry(root, width=10, font=48)
entry2.grid(row=2, column=1)
L3 = tk.Label(root, text="Scannumber", font=48)
L3.grid(row=3, column=0)
entry3 = tk.Entry(root, width=10, font=48)
entry3.grid(row=3, column=1)
L4 = tk.Label(root, text="Pixelnumber", font=48)
L4.grid(row=4, column=0)
entry4 = tk.Entry(root, width=10, font=48)
entry4.grid(row=4, column=1)

button = tk.Button(master=root, text="Plot", width=10, font=48, command=plot)
button.grid(row=5, column=0, columnspan=2)

text1 = tk.Text(root, height=18, width=30, font=36)
text1.grid(row=6, column=0, columnspan=2, sticky="nwes", padx=10, pady=10)

fig = plt.figure(figsize=(4.8 * 3, 3.6 * 2))

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().grid(
    row=1, column=2, rowspan=6, columnspan=2, sticky="nwes", padx=10, pady=10
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
root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
tk.mainloop()
