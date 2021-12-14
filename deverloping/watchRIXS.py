import time
from watchdog.observers import Observer
from watchdog.events import *
import os
import h5py
import numpy as np


def newFile(fileDir):
    list = os.listdir(fileDir)
    list.sort(key=lambda fn: os.path.getmtime(fileDir + fn))
    print(list[-1])
    return list[-1]


def getInfo(filename):
    global path
    f = h5py.File(path + filename, "r")

    PhotonEnergy = round(
        np.mean(f["entry"]["instrument"]["NDAttributes"]["PhotonEnergy"][()]), 3
    )
    PolarMode = np.mean(f["entry"]["instrument"]["NDAttributes"]["PolarMode"][()])
    # if PolarMode == 0:
    #     Polarization = "LH"
    # elif PolarMode == 1:
    #     Polarization = "LV"
    # elif PolarMode == 2:
    #     Polarization = "C+"
    # else:
    #     Polarization = "C-"

    Temp = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleTemp"][()]), 2)

    xx = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleX"][()]), 4)
    yy = round(np.mean(f["entry"]["instrument"]["NDAttributes"]["SampleY"][()]), 4)
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
        PhotonEnergy,
        PolarMode,
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


class FileEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        pass

    def on_moved(self, event):
        if event.is_directory:
            print(
                "directory moved from {0} to {1}".format(
                    event.src_path, event.dest_path
                )
            )
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))
            # getInfo(newFile(path))

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))


if __name__ == "__main__":

    path = "C:\\Researches\\Scripts\\plotRIXS\\"
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
