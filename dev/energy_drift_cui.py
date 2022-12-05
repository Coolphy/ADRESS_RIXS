# %%
import tkinter as tk
from tkinter import filedialog

import h5py
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit


# %%
def load_h5(fileName):
    f = h5py.File(fileName, "r")
    ccd = np.array(f["entry"]["analysis"]["spectrum"][()])
    energy = np.mean(f["entry"]["instrument"]["NDAttributes"]["PhotonEnergy"][()])
    return ccd, energy


def load_data(fileList):
    rixs_dict = {}
    for i, fileName in enumerate(fileList):
        rixs_dict[i] = {}
        rixs_dict[i]["FileName"] = fileName
        try:
            rixs_dict[i]["detector"] = fileName[-5:-3]
            rixs_dict[i]["ccd"], rixs_dict[i]["energy"] = load_h5(fileName)
        except:
            pass
    return rixs_dict


def gaussian_amp(x, xc, fwhm, amp):
    return amp * np.exp(-4 * np.log(2) * (x - xc) ** 2 / fwhm**2)


def fit_peak(data):
    center = np.argmax(data)
    amp = np.max(data)
    xdata = np.arange(len(data))
    popt, pcov = curve_fit(gaussian_amp, xdata, data, p0=[center, 10.0, amp])
    perr = np.sqrt(np.diag(pcov))
    return popt, perr


def fit_data(rixs_dict):
    for i, key in enumerate(rixs_dict):
        try:
            rixs_dict[key]["popt"], rixs_dict[key]["perr"] = fit_peak(
                rixs_dict[key]["ccd"]
            )
        except:
            pass
    return rixs_dict


def reform_data(rixs_dict):
    lens = int(len(rixs_dict) / 3)
    data = {}
    data["energy"] = np.zeros(lens)
    data["center1"] = np.zeros(lens)
    data["center2"] = np.zeros(lens)
    data["center3"] = np.zeros(lens)
    data["width1"] = np.zeros(lens)
    data["width2"] = np.zeros(lens)
    data["width3"] = np.zeros(lens)

    i = 0
    j = 0
    k = 0

    for key in rixs_dict:
        if rixs_dict[key]["detector"] == "d1":
            data["energy"][i] = rixs_dict[key]["energy"]
            data["center1"][i] = rixs_dict[key]["popt"][0]
            data["width1"][i] = rixs_dict[key]["popt"][1]
            i = i + 1
        elif rixs_dict[key]["detector"] == "d2":
            data["center2"][j] = rixs_dict[key]["popt"][0]
            data["width2"][j] = rixs_dict[key]["popt"][1]
            j = j + 1
        elif rixs_dict[key]["detector"] == "d3":
            data["center3"][i] = rixs_dict[key]["popt"][0]
            data["width3"][i] = rixs_dict[key]["popt"][1]
            k = k + 1
    return data


# %%
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    fileList = list(
        filedialog.askopenfilenames(
            title="Select ADRESS data files", filetypes=[("HDF5 files", "*.h5")]
        )
    )

    rixs = load_data(fileList)
    rixs = fit_data(rixs)

# %%
data  = reform_data(rixs)
# %%
