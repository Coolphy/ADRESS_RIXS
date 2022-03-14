import os
import h5py
import numpy as np
import csv
import tkinter as tk
from tkinter import filedialog


def listFile(fileDir):
    list = sorted(os.listdir(fileDir))
    # list.sort(key=lambda fn: os.path.getmtime(fileDir + fn))
    return list


def getInfo(filename):
    global path
    f = h5py.File(path + "\\" + filename, "r")

    PhotonEnergy = round(
        np.mean(f["entry"]["instrument"]["NDAttributes"]["PhotonEnergy"][()]), 2
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

    xx = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleXs"][()]), 3)
    yy = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleYs"][()]), 3)
    zz = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleZ"][()]), 3)
    Tht = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTheta"][()]), 2)
    Phi = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SamplePhi"][()]), 2)
    Tilt = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTilt"][()]), 2)

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
    path = filedialog.askdirectory(title="Select data path")
    # print(path)
    logdir = os.path.abspath(os.path.dirname(path))
    # print(logdir)

    # path = "C:\\Researches\\Data\\VI3\\202107"
    # path = os.path.split(os.path.realpath(__file__))[0]
    f = open(logdir + "\\logbook.csv", "w", newline="")
    writer = csv.writer(f)
    fileList = listFile(path)
    writer.writerow(
        [
            "Files",
            "Energy(eV)",
            "Polar",
            "Temperature(K)",
            "X(mm)",
            "Y(mm)",
            "Z(mm)",
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
        try:
            writer.writerow(getInfo(x))
        except:
            print("file " + str(x) + " is broken!")
        continue
