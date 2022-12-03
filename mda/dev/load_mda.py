# %%
from mda import *
import numpy as np


class load_mda:
    def __init__(self):
        self.x = np.array([])
        self.y = np.array([])
        self.header = ""

    def load_data(self, fileName):
        d = readMDA(fileName)

        self.x = np.zeros([d[1].curr_pt, len(d[1].p)])
        self.y = np.zeros([d[1].curr_pt, len(d[1].d)])

        for j in range(len(d[1].p)):
            self.header = self.header + f"{d[1].p[j].name.decode('utf-8')},\t"
        for j in range(len(d[1].d)):
            self.header = self.header + f"{d[1].d[j].name.decode('utf-8')},\t"

        for i in range(d[1].curr_pt):
            for j in range(len(d[1].p)):
                self.x[i, j] = d[1].p[j].data[i]
            for j in range(len(d[1].d)):
                self.y[i, j] = d[1].d[j].data[i]
        return self.x, self.y

    def save_data(self, fileName):
        numpy.savetxt(
            fileName,
            np.hstack((self.x, self.y)),
            fmt="%.18e",
            delimiter=",\t",
            newline="\n",
            header=self.header,
            footer="",
            comments="# ",
            encoding=None,
        )


if __name__ == "__main__":
    fileName = "C:/Researches/Scripts/gnuplot/mda/X03MA_PC_0017"
    s = load_mda()
    s.load_data(f"{fileName}.mda")
    print(np.shape(s.x))
    print(np.shape(s.y))
    s.save_data(f"{fileName}.txt")
