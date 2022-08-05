```python
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def get_xas(scanNumber):
    global projectPath
    global baseAtom
    if scanNumber < 10:
        filename = baseAtom+'_'+'000'+str(scanNumber)
    elif scanNumber < 100:
        filename = baseAtom+'_'+'00'+str(scanNumber)
    elif scanNumber < 1000:    
        filename = baseAtom+'_'+'0'+str(scanNumber)
    else:    
        filename = baseAtom+'_'+str(scanNumber)
    data = np.loadtxt(projectPath+'/XAS/'+filename+'.xas', comments='#')
    photonEnergy = data[:,0]
    tey = data[:,1]
    tfy = data[:,2]
    rmu = data[:,3]
    return photonEnergy,tey,tfy,rmu

def elastic_shift(pixelData):
    global energyDispersion
    peaks, _ = signal.find_peaks(pixelData,height=10,width=6)
    xdataPixel = np.arange(len(pixelData))
    xdataPixel = xdataPixel[(peaks[-1]-2000):(peaks[-1]+200)]
    energyData = pixelData[(peaks[-1]-2000):(peaks[-1]+200)]
    xDataEnergy = (xdataPixel - peaks[-1]) * energyDispersion * -1
    return xDataEnergy,energyData

def x_corr(refData, uncorrData):
    corr = signal.correlate(refData, uncorrData)
    lag = np.argmax(corr)
    corrData = np.roll(uncorrData, lag)
    return corrData

def get_rixs(scannumber):
    global projectPath
    global baseAtom
    if scannumber < 10:
        filename = baseAtom+'_'+'000'+str(scannumber)
    elif scannumber < 100:
        filename = baseAtom+'_'+'00'+str(scannumber)
    elif scannumber < 1000:    
        filename = baseAtom+'_'+'0'+str(scannumber)
    else:    
        filename = baseAtom+'_'+str(scannumber)
    f1 = h5py.File(projectPath+'/RIXS/'+filename+'_d1.h5', 'r')
    f2 = h5py.File(projectPath+'/RIXS/'+filename+'_d2.h5', 'r')
    f3 = h5py.File(projectPath+'/RIXS/'+filename+'_d3.h5', 'r')
    ccd1 = np.array(f1['entry']['analysis']['spectrum'][()])
    ccd2 = np.array(f2['entry']['analysis']['spectrum'][()])
    ccd3 = np.array(f3['entry']['analysis']['spectrum'][()])
    ccd1 = x_corr(ccd2,ccd1)
    ccd3 = x_corr(ccd2,ccd3)
    xdata,tempData = elastic_shift(ccd1+ccd2+ccd3)
    return xdata,tempData

def combine_rixs(scans):
    for i,scannumber in enumerate(scans):
        if i == 0:
            xdata,ydata = get_rixs(scannumber)
            refdata = ydata
            sumdata = ydata
        else:
            _,ydata = get_rixs(scannumber)
            ydata = x_corr(refdata,ydata)
            sumdata = sumdata+ydata
    return xdata,sumdata

if __name__ == "__main__":
    projectPath = 'X:/RIXS/Asmara'
    baseAtom = 'O'
    energyDispersion = 0.00535 #eV/subpixel

```

