import numpy as np
import h5py

from scipy.signal import correlate, correlation_lags


class rixs_tools(object):
    def __init__(self, *args):
        pass

    def load_ccd(self, file_name):

        f = h5py.File(file_name, "r")
        ccd = np.array(f["entry"]["analysis"]["spectrum"][()])
        f.close()

        return ccd

    def x_corr(self, refData, uncorrData, xrange=(0, 6000)):

        xData = np.arange(len(refData))

        tempref = refData[(xData > xrange[0]) & (xData < xrange[1])]
        tempuncorr = uncorrData[(xData > xrange[0]) & (xData < xrange[1])]

        corr = correlate(tempref, tempuncorr)
        lags = correlation_lags(len(tempref), len(tempuncorr))
        lag = lags[np.argmax(corr)]
        corrData = np.roll(uncorrData, lag)

        return corrData

    def polar_trans(self, PolarMode):
        if PolarMode == 0:
            Polarization = "LH"
        elif PolarMode == 1:
            Polarization = "LV"
        elif PolarMode == 2:
            Polarization = "C+"
        else:
            Polarization = "C-"
        return Polarization

    def load_meta(self, file_name):
        useful_strings = [
            "PhotonEnergy",
            "PolarMode",
            "SampleTemp",
            "SampleXs",
            "SampleYs",
            "SampleZ",
            "SampleTheta",
            "SamplePhi",
            "SampleTilt",
            "AcquireTime",
            "ExposureSplit",
            "ExitSlit",
            "BeamCurrent",
        ]
        f = h5py.File(file_name, "r")
        meta_data = {}
        NDAttributes = f["entry"]["instrument"]["NDAttributes"]
        meta_data["FileName"] = file_name
        for key in useful_strings:
            meta_data[key] = round(np.mean(NDAttributes[key]), 3)
        meta_data["PolarMode"] = self.polar_trans(meta_data["PolarMode"])
        f.close()
        return meta_data
