```python
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
# from scipy.optimize import curve_fit

path = 'X:\\RIXS\\InHouse_e18695\\CrCl3_Jan_2022\\RIXS\\'
base = 'Cr'
energyDispersion = 0.00535 #eV/subpixel

```


```python
def elasticShift(pixelData):

    global energyDispersion

    peaks, _ = signal.find_peaks(pixelData,height=10,width=6)
    xdataPixel = np.arange(len(pixelData))
    
    xdataPixel = xdataPixel[(peaks[-1]-2000):(peaks[-1]+200)]
    energyData = pixelData[(peaks[-1]-2000):(peaks[-1]+200)]
    
    xDataEnergy = (xdataPixel - peaks[-1]) * energyDispersion * -1

    return [xDataEnergy,energyData]

def xCorr(refData, uncorrData):

    corr = signal.correlate(refData, uncorrData)
    lag = np.argmax(corr)
    corrData = np.roll(uncorrData, lag)

    return corrData

def getData(scannumber):
    global path
    global base
    
    if scannumber < 10:
        filename = base+"_"+"000"+str(scannumber)
    elif scannumber < 100:
        filename = base+"_"+"00"+str(scannumber)
    elif scannumber < 1000:    
        filename = base+"_"+"0"+str(scannumber)
    else:    
        filename = base+"_"+str(scannumber)

    f1 = h5py.File(path+filename+"_d1.h5", 'r')
    f2 = h5py.File(path+filename+"_d2.h5", 'r')
    f3 = h5py.File(path+filename+"_d3.h5", 'r')

    ccd1 = f1['entry']['analysis']['spectrum'][()]
    ccd2 = f2['entry']['analysis']['spectrum'][()]
    ccd3 = f3['entry']['analysis']['spectrum'][()]
    
    ccd1 = xCorr(ccd2,ccd1)
    ccd3 = xCorr(ccd2,ccd3)
    xdata,tempData = elasticShift(ccd1+ccd2+ccd3)
    
    return [xdata,tempData]

def getScan(scans):
    for i,scannumber in enumerate(scans):
        if i == 0:
            [xdata,ydata] = getData(scannumber)
            refdata = ydata
            sumdata = ydata
        else:
            [_,ydata] = getData(scannumber)
            ydata = xCorr(refdata,ydata)
            sumdata = sumdata+ydata
    return [xdata,sumdata]

```

