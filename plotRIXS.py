import numpy as np
import matplotlib.pyplot as plt
import h5py
from scipy import optimize
from scipy import signal
from scipy.signal.signaltools import choose_conv_method
#%matplotlib nbagg

def MakeFileName( scanNumber ):
    global baseAtom
    if scanNumber < 10:
        fileName = baseAtom+"_"+"000"+str(scanNumber)
    elif scanNumber < 100:
        fileName = baseAtom+"_"+"00"+str(scanNumber)
    elif scanNumber < 1000:    
        fileName = baseAtom+"_"+"0"+str(scanNumber)
    else:    
        fileName = baseAtom+"_"+str(scanNumber)
    return fileName

def EnergyTrans( pixelData ):
    global energyResolution
    energyData = np.array([pixelData[0,:]*energyResolution,pixelData[1,:]])
    return energyData

def xCorr( refData,corrData ):
    corr = signal.correlate(refData,corrData)
    lags = signal.correlation_lags(len(refData),len(corrData))
    lag = lags[np.argmax(corr)]
    return lag

def GetData( scanNumber ):
    global myPath
    f1 = h5py.File(myPath+MakeFileName( scanNumber )+"_d1.h5", 'r')
    f2 = h5py.File(myPath+MakeFileName( scanNumber )+"_d2.h5", 'r')
    f3 = h5py.File(myPath+MakeFileName( scanNumber )+"_d3.h5", 'r')  
    ccd1 = f1['entry']['analysis']['spectrum'][()]
    ccd2 = f2['entry']['analysis']['spectrum'][()]
    ccd3 = f3['entry']['analysis']['spectrum'][()]
    ccd = np.roll(ccd1,xCorr(ccd2,ccd1))+ccd2+np.roll(ccd3,xCorr(ccd2,ccd3))
#    xData = np.arange(len(ccd))
#    rawData = np.array([xData,ccd])
    return ccd

baseAtom = 'V'
refEnergy = 778 #eV
energyResolution = 0.0100 #eV
myPath = 'C:\\Researches\\Data\\CsVSb_Jun_2021\\RIXS\\'

scanNumber = 19
tempData=GetData( scanNumber )
plt.figure()
plt.plot(tempData)
plt.xlim(3000,4000)
plt.show()

refElasticPixel = 3100

zipLog = {
    'LV_512p6':np.arange(38,49+1),
    'LV_513p6':np.append(np.arange(50,58+1),np.arange(64,73+1)),
    'LV_515p9':np.arange(76,85+1)}

for key in zipLog:
    data = refData = GetData(zipLog[key][0])
    for x in zipLog[key][1:]:
        tempData = GetData(x)
        data = data + np.roll(tempData,xCorr(refData,tempData))
    pixelData = globals()[key] = data/len(zipLog[key])
    plt.figure()
    plt.plot(pixelData,label=key)
    plt.legend()
#    plt.xlim(3000,4000)
    plt.show()