# %%
from mda import *
import numpy as np


class load_mda:
    def __init__(self):
        self.x = np.array([])
        self.y = np.array([])
        self.header = ""

    def load_data(self, fileName):

        d = readMDA(fileName, useNumpy=True)

        self.rank = d[1].rank

        if self.rank == 1:

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

        elif self.rank == 2:

            self.shape = np.shape(d[2].d[0].data)

            self.x = np.zeros([d[2].curr_pt, d[1].curr_pt, len(d) - 1])
            self.y = np.zeros([d[2].curr_pt, d[1].curr_pt, len(d[2].d)])

            for pos in range(len(d) - 1):
                self.header = self.header + f"{d[pos+1].p[0].name.decode('utf-8')},\t"
            for det in range(len(d[2].d)):
                self.header = self.header + f"{d[2].d[det].name.decode('utf-8')},\t"

            pos_1 = d[1].curr_pt
            pos_2 = d[2].curr_pt

            for i in range(pos_1):
                for j in range(pos_2):
                    self.x[j, i, 0] = d[1].p[0].data[i]
                    self.x[j, i, 1] = d[2].p[0].data[0, j]

            for det in range(len(d[2].d)):
                for i in range(pos_1):
                    for j in range(pos_2):
                        self.y[j, i, det] = d[2].d[det].data[i, j]

    def save_data(self, fileName):

        if self.rank == 1:

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

        elif self.rank == 2:

            with open(fileName, "w") as file:
                file.writelines(f"#\t{self.header}\n")
                for i in range(self.shape[0]):
                    for j in range(self.shape[1]):
                        for xx in self.x[j, i, :]:
                            file.writelines(f"{xx:6e}\t")
                        for yy in self.y[j, i, :]:
                            file.writelines(f"{yy:6e}\t")
                        file.writelines("\n")
                    file.writelines("\n")

            file.close()


if __name__ == "__main__":
    fileName = "C:/Researches/Scripts/gnuplot/mda/X03MA_PC_0044"
    s = load_mda()
    s.load_data(f"{fileName}.mda")
    print(np.shape(s.x))
    print(np.shape(s.y))
    print(np.shape(np.hstack((s.x, s.y))))
    s.save_data(f"{fileName}.txt")

    # %%
    a = np.arange(21)
    b = np.arange(51)
    c = np.tile(b, (21, 1))
    # %%
    print(a, b, c)
# %%
