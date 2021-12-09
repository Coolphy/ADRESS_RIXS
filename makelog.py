import os
import h5py
import numpy as np


def listFile(fileDir):
    list = os.listdir(fileDir)
    # list.sort(key=lambda fn: os.path.getmtime(fileDir + fn))
    # print(list[-1])
    return list


def getInfo(filename):
    global path
    f = h5py.File(path + filename, "r")

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

    Temp = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTemp"][()]), 2)

    xx = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleXs"][()]), 4)
    yy = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleYs"][()]), 4)
    zz = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleZ"][()]), 4)
    Tht = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTheta"][()]), 3)
    Phi = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SamplePhi"][()]), 3)
    Tilt = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTilt"][()]), 3)

    AcqTime = np.mean(f["entry"]["instrument"]["NDAttributes"]["AcquireTime"][()])
    SplitTime = np.mean(f["entry"]["instrument"]["NDAttributes"]["ExposureSplit"][()])
    Ring = round(
        np.mean(f["entry"]["instrument"]["NDAttributes"]["BeamCurrent"][()]), 0
    )
    fileInfo = [
        filename,
        PhotonEnergy,
        Polarization,
        Temp,
        xx,
        yy,
        zz,
        Tht,
        Phi,
        Tilt,
        AcqTime,
        SplitTime,
        Ring,
    ]
    print(fileInfo)


if __name__ == "__main__":
    path = "C:\\Researches\\Scripts\\plotRIXS\\test\\"
    fileList = listFile(path)
    print(
        "Filename,PhotonEnergy,Polarization,Temp,xx,yy,zz,Tht,Phi,Tilt,AcqTime,SplitTime,Ring"
    )

    for x in fileList:
        getInfo(x)
