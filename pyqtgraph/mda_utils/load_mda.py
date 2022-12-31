# %%
from .mda import *
import numpy as np


class load_mda:
    def __init__(self):

        self.data = {}
        self.head = {}

    def load(self, fileName):

        d = readMDA(fileName, useNumpy=True)

        dim = len(d) - 1
        self.data["dimension"] = dim
        self.data["positioners"] = {}
        self.data["detectors"] = {}

        self.data["shape"] = np.shape(d[dim].p[0].data)

        for p_n in range(dim):
            self.data["positioners"][p_n] = {}
            self.data["positioners"][p_n][
                "name"
            ] = f"{d[p_n+1].p[0].name.decode('utf-8')}"
            self.data["positioners"][p_n]["data"] = d[p_n + 1].p[0].data

        for d_n in range(len(d[dim].d)):
            self.data["detectors"][d_n] = {}
            self.data["detectors"][d_n][
                "name"
            ] = f"{d[dim].d[d_n].name.decode('utf-8')}"
            self.data["detectors"][d_n]["data"] = d[dim].d[d_n].data

        self.reform()

    def reform(self):
        for low_dim_total in range(len(self.data["positioners"])):
            for low_dim in range(low_dim_total):
                self.data["positioners"][low_dim]["data"] = np.transpose(
                    np.tile(
                        self.data["positioners"][low_dim]["data"],
                        (self.data["shape"][low_dim + 1], 1),
                    )
                )

    def save(self, fileName):
        for p in self.data["positioners"]:
            numpy.savetxt(
                f"{fileName}_P{p}.txt",
                self.data["positioners"][p]["data"],
                fmt="%.18e",
                delimiter=",\t",
                newline="\n",
                header=self.data["positioners"][p]["name"],
                footer="",
                comments="# ",
                encoding=None,
            )
        for d in self.data["detectors"]:
            numpy.savetxt(
                f"{fileName}_D{d}.txt",
                self.data["detectors"][d]["data"],
                fmt="%.18e",
                delimiter=",\t",
                newline="\n",
                header=self.data["detectors"][d]["name"],
                footer="",
                comments="# ",
                encoding=None,
            )


# %%
if __name__ == "__main__":

    fileName = "C:/Researches/Data/VI3/202211/MDA/X03MA_PC_0022"
    s = load_mda()
    s.load(f"{fileName}.mda")
    s.save(fileName)
# %%
