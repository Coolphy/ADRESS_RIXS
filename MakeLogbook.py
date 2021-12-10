import os
import h5py
import numpy as np
import csv
import tkinter as tk
from tkinter import filedialog


def listFile(fileDir):
    list = os.listdir(fileDir)
    # list.sort(key=lambda fn: os.path.getmtime(fileDir + fn))
    return list


def getInfo(filename):
    global path
    f = h5py.File(path + "\\RIXS\\" + filename, "r")

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
    ExitSlit = np.mean(f["entry"]["instrument"]["NDAttributes"]["ExitSlit"][()])
    Ring = round(
        np.mean(f["entry"]["instrument"]["NDAttributes"]["BeamCurrent"][()]), 0
    )
    fileInfo = [
        filename[:-6],
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
        ExitSlit,
        Ring,
    ]
    return fileInfo


if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    print(path)

    # path = "C:\\Researches\\Data\\VI3\\202107"
    # path = os.path.split(os.path.realpath(__file__))[0]
    f = open(path + "\\logbook.csv", "w", newline="")
    writer = csv.writer(f)
    fileList = listFile(path + "\\RIXS\\")
    writer.writerow(
        [
            "Files",
            "PhotonEnergy(eV)",
            "Polarization",
            "Temperature(K)",
            "SampleX(mm)",
            "SampleY(mm)",
            "SampleZ(mm)",
            "Theta",
            "Phi",
            "Tilt",
            "AcqTime(s)",
            "SplitTime(s)",
            "Slit(um)",
            "RingCurrent",
        ]
    )

    for x in fileList[::3]:
        writer.writerow(getInfo(x))
