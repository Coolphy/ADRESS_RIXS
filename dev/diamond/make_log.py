# %%
import os
import h5py
import numpy as np
import csv
import tkinter as tk
from tkinter import filedialog

import time
import datetime


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


def listFile(fileDir):
    fileExt = '.nxs'
    list = sorted([_ for _ in os.listdir(fileDir) if _.endswith(fileExt)])
    # list.sort(key=lambda fn: os.path.getmtime(fileDir + fn))
    return list


def getInfo(filename):
    global path
    f = h5py.File(path + "\\" + filename, "r")

    PhotonEnergy = round(f["entry"]["instrument"]["pgm"]["energy"][()], 2)
    Polarization = f["entry"]["instrument"]["id"]["polarisation"][()]

    Temp = round(f["entry"]["instrument"]["lakeshore336"]["sample"][()], 2)
    xx = round(f["entry"]["instrument"]["manipulator"]["x"][()], 4)
    yy = round(f["entry"]["instrument"]["manipulator"]["y"][()], 4)
    zz = round(f["entry"]["instrument"]["manipulator"]["z"][()], 4)
    Tht = round(f["entry"]["instrument"]["manipulator"]["th"][()], 4)
    Phi = round(f["entry"]["instrument"]["manipulator"]["phi"][()], 4)
    Tilt = round(f["entry"]["instrument"]["manipulator"]["chi"][()], 4)

    armtth = round(f["entry"]["instrument"]["spectrometer"]["armtth"][()], 4)
    specgamma = round(
        f["entry"]["instrument"]["spectrometer"]["specgamma"][()])
    slit = round(f["entry"]["instrument"]["s5"]["v1_gap"][()], 1)
    # current = round(np.mean(f["entry"]["m4c1"]["m4c1"][()]), 4)
    count_time = round(
        np.mean(f["entry"]["instrument"]["andor"]["count_time"][()]))
    images = len(f["entry"]["andor"]["ds"][()])

    Date = get_FileCreateTime(path + "\\" + filename)
    Command = f["entry"]["scan_command"][()]
    fileInfo = [
        filename[4:-4],
        PhotonEnergy,
        Polarization.decode(),
        Temp,
        xx,
        yy,
        zz,
        Tht,
        Phi,
        Tilt,
        armtth,
        specgamma,
        slit,
        # current,
        count_time,
        images,
        Date,
        Command.decode(),
    ]
    return fileInfo


if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title="Select data path")

    # logdir = os.path.abspath(os.path.dirname(path))
    # print(logdir)

    f = open(path + "\\logbook.csv", "w", newline="")
    writer = csv.writer(f)
    fileList = listFile(path)
    writer.writerow([
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
        'Armtth',
        'Specgamma',
        'slit',
        'M4current',
        'Images',
        'Date',
        'Command',
    ])

    for x in fileList:
        try:
            writer.writerow(getInfo(x))
        except:
            print("file " + str(x) + " is not RIXS!")

    f.close()
    print("Logbook is saved in " + path)
