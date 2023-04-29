import h5py
import numpy as np
from scipy.signal import correlate, correlation_lags, find_peaks


class adress_rixs:
    def __init__(self, path="", base="", dispersion=1.0):
        self.xas_dict = {}
        self.rixs_dict = {}
        self.path = path
        self.base = base
        self.dispersion = dispersion
        self.elastic_peak()

    def load_xas(self, scan_number):
        if scan_number not in self.xas_dict:
            xas = {}
            data = np.loadtxt(
                f"{self.path}/XAS/{self.base}_{scan_number:04d}.xas", comments="#"
            )
            xas["EN"] = data[:, 0]
            xas["TEY"] = data[:, 1]
            xas["TFY"] = data[:, 2]
            xas["RMU"] = data[:, 3]
            self.xas_dict[scan_number] = xas
        else:
            xas = self.xas_dict[scan_number]

        return xas["EN"], xas["TEY"], xas["TFY"], xas["RMU"]

    def load_h5(self, file_name):
        f = h5py.File(file_name, "r")
        ccd = np.array(f["entry"]["analysis"]["spectrum"][()])
        f.close()

        return ccd

    def load_ccds(self, scan_number):
        if scan_number not in self.rixs_dict:
            rixs = {}
            for i in range(1, 4):
                rixs[i] = self.load_h5(
                    f"{self.path}/RIXS/{self.base}_{scan_number:04d}_d{i}.h5"
                )
            self.rixs_dict[scan_number] = rixs
        else:
            rixs = self.rixs_dict[scan_number]

        return rixs[1], rixs[2], rixs[3]

    def x_corr(self, refData, uncorrData):
        corr = correlate(refData, uncorrData)
        lags = correlation_lags(len(refData), len(uncorrData))
        lag = lags[np.argmax(corr)]
        corrData = np.roll(uncorrData, lag)

        return corrData

    def elastic_peak(self, center=None, height=10, width=3):
        self.zeropixel = center
        self.elastic_height = height
        self.elastic_width = width

    def elastic_shift(self, pixelData):
        xdataPixel = np.arange(len(pixelData))

        if self.zeropixel is None:
            try:
                # try to find peak
                peaks, _ = find_peaks(
                    pixelData, height=self.elastic_height, width=self.elastic_width
                )

                # try to find peak with right edge
                # peaks = xdataPixel[pixelData>height]
            except:
                peaks = [len(xdataPixel) - 200]

        else:
            peaks = [self.zeropixel]

        # chop data
        xdataPixel = xdataPixel[(peaks[-1] - 2000) : (peaks[-1] + 200)]
        energyData = pixelData[(peaks[-1] - 2000) : (peaks[-1] + 200)]

        xDataEnergy = (xdataPixel - peaks[-1]) * self.dispersion

        return xDataEnergy, energyData

    def load_rixs(self, scan_number):
        ccd1, ccd2, ccd3 = self.load_ccds(scan_number)
        ccd1 = self.x_corr(ccd2, ccd1)
        ccd3 = self.x_corr(ccd2, ccd3)
        xdata = np.arange(len(ccd2))
        tempdata = ccd1 + ccd2 + ccd3

        #     shift automaticlly
        xdata, tempdata = self.elastic_shift(tempdata)

        return xdata, tempdata

    def load_runs(self, scans):
        for i, scan_number in enumerate(scans):
            if i == 0:
                xdata, ydata = self.load_rixs(scan_number)
                refdata = ydata
                sumdata = ydata
            else:
                _, ydata = self.load_rixs(scan_number)
                ydata = self.x_corr(refdata, ydata)
                sumdata = sumdata + ydata

        # normalize data
        # sumdata = sumdata / len(scans)

        return xdata, sumdata

    def plot_map(self, run_list, Y=None):
        run_num = len(run_list)
        data = np.zeros((run_num, 2200))
        for i, runs in enumerate(run_list):
            if type(runs) is list:
                X, d = self.load_runs(runs)
            else:
                X, d = self.load_runs([runs])
            data[i, :] = d
        if Y is None:
            Y = np.arange(run_num + 1)
        else:
            pass
        fig, ax = subplots()
        im = ax.pcolorfast(X, Y, data)
        fig.colorbar(im)
        ax.set_xlabel("Energy Loss ( eV )")

        return fig, ax, im


if __name__ == "__main__":
    project_path = "X:/RIXS/Asmara/"
    base_atom = "O"
    energy_dispersion = 0.00457  # eV/subpixel

    rixs = adress_rixs(path=project_path, base=base_atom, dispersion=energy_dispersion)
