# %%
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate
from scipy.optimize import curve_fit
from scipy.optimize import least_squares

Path = 'C:\\Researches\\Data\\Fe3-xGeTe2\\202201\\RIXS' 
Atom = 'Fe'
Scan = 26

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

def lsq_poly2(x, t, y):
    return y - (x[0] * t ** 2 + x[1] * t + x[2])

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
        ((poly2(xdata, *popt) - 100) < ydata) & (ydata < (poly2(xdata, *popt) + 100))
    ]
    ydata3 = ydata[
        ((poly2(xdata, *popt) - 100) < ydata) & (ydata < (poly2(xdata, *popt) + 100))
    ]
    popt, _ = curve_fit(poly2, xdata3, ydata3)

    xdata4 = xdata[
        ((poly2(xdata, *popt) - 50) < ydata) & (ydata < (poly2(xdata, *popt) + 50))
    ]
    ydata4 = ydata[
        ((poly2(xdata, *popt) - 50) < ydata) & (ydata < (poly2(xdata, *popt) + 50))
    ]
    popt, _ = curve_fit(poly2, xdata4, ydata4)

    xdata5 = xdata[
        ((poly2(xdata, *popt) - 20) < ydata) & (ydata < (poly2(xdata, *popt) + 20))
    ]
    ydata5 = ydata[
        ((poly2(xdata, *popt) - 20) < ydata) & (ydata < (poly2(xdata, *popt) + 20))
    ]
    popt, _ = curve_fit(poly2, xdata5, ydata5)
    
    x0=np.array([*popt])
    res_robust = least_squares(lsq_poly2, x0, loss='soft_l1', f_scale=0.1, args=(xdata5, ydata5))
    print(res_robust.x)
    return res_robust.x


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


def GetLength(scanNumber):
    global Path
    f1 = h5py.File(Path + "/" + MakeFileName(scanNumber) + "_d1.h5", "r")
    roiY = f1["entry"]["instrument"]["NDAttributes"]["ROIArraySizeY"][()]
    roi = np.mean(roiY)
    return roi

# %%
ccd1, ccd2, ccd3 = GetData(Scan)
DataLength = int(GetLength(Scan))

fig = plt.figure()
fig.add_subplot(231).scatter(*np.transpose(ccd1), s=0.2)
fig.add_subplot(232).scatter(*np.transpose(ccd2), s=0.2)
fig.add_subplot(233).scatter(*np.transpose(ccd3), s=0.2)

print('x ** 2, x, y0')

p1 = curventureFit(*np.transpose(ccd1))
p2 = curventureFit(*np.transpose(ccd2))
p3 = curventureFit(*np.transpose(ccd3))

xAxis = np.arange(1632)
plt.subplot(231).plot(xAxis, poly2(xAxis, *p1), c="r")
plt.subplot(232).plot(xAxis, poly2(xAxis, *p2), c="r")
plt.subplot(233).plot(xAxis, poly2(xAxis, *p3), c="r")

ccd1 = curventureSubtract(ccd1, p1)
ccd2 = curventureSubtract(ccd2, p2)
ccd3 = curventureSubtract(ccd3, p3)

xedges = np.array([1,1634])
yedges = np.linspace(0,DataLength,DataLength *4+1)

line1, xedges, yedges = np.histogram2d(*np.transpose(ccd1), bins=(1, yedges))
line2, xedges, yedges = np.histogram2d(*np.transpose(ccd2), bins=(1, yedges))
line3, xedges, yedges = np.histogram2d(*np.transpose(ccd3), bins=(1, yedges))

xPixel = np.arange(DataLength * 4)
fig.add_subplot(234).scatter(xPixel, *line1, s=0.5)
fig.add_subplot(235).scatter(xPixel, *line2, s=0.5)
fig.add_subplot(236).scatter(xPixel, *line3, s=0.5)

print('xc, fwhm, amp, y0')

fit1 = peakFit(np.array(*line1))
fit2 = peakFit(np.array(*line2))
fit3 = peakFit(np.array(*line3))

plt.subplot(234).plot(xPixel, Gaussian_amp(xPixel, *fit1), c="r")
plt.subplot(235).plot(xPixel, Gaussian_amp(xPixel, *fit2), c="r")
plt.subplot(236).plot(xPixel, Gaussian_amp(xPixel, *fit3), c="r")

plt.show()


# %%
