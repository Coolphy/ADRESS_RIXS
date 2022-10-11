import sys
import os
import time
from h5py import File
import numpy as np
import matplotlib.pyplot as plt
import threading
import tkinter as tk
from tkinter import filedialog

class watch_rixs():
    def __init__(self,fileDir):
        self.fig = plt.figure(figsize=(6.4, 4.8), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.fileDir = fileDir
        self.fileName = sorted(os.listdir(self.fileDir))[-1]
        self.ax.set_xlim(0,6000)

        # self.bx = self.fig.add_subplot(122)
        # self.bx.set_xticks([])
        # self.bx.set_yticks([])

    def update_plot(self):
        self.fileName = sorted(os.listdir(self.fileDir))[-1]
        h5File = adress_rixs(self.fileDir+'/'+self.fileName)
        xdata,ydata = h5File.load_data()

        xmin, xmax = self.ax.get_xlim()
        # ymin, ymax = self.ax.get_ylim()

        self.ax.cla()
        self.ax.plot(xdata, ydata)
        self.ax.set_xlim(xmin, xmax)
        # self.ax.set_ylim(ymin, ymax)
        self.ax.set_title(str(self.fileName))

        # meta_data = h5File.load_meta()
        # for key in meta_data:
        #     meta_print = meta_print + key+' = '+meta_data[key]+'\n'

        # self.bx.text(0, 1, meta_print, ha='left',wrap=True)

        plt.draw()

    def show_plot(self):
        plt.show() 

class adress_rixs():

    def __init__(self,fileName):
        self.f = File(fileName,'r')

    def load_data(self):
        ccd = self.f["entry"]["analysis"]["spectrum"][()]
        xdata = np.arange(len(ccd))
        return xdata, ccd

    def load_meta(self):
        meta_data = {}
        NDAttributes = self.f['entry']['instrument']['NDAttributes']
        for key in NDAttributes:
            meta_data[key] = round(np.mean(NDAttributes[key]),3)
        return meta_data

def update_plot(w):
    global quit_flag
    while(1):
        if quit_flag:
            break
        try:
            w.update_plot()
        except:
            continue
        time.sleep(3)

def main(fileDir):
    global quit_flag
    quit_flag = False
    w = watch_rixs(fileDir)
    t = threading.Thread(target=update_plot, args=(w,))
    t.start()
    w.show_plot()
    quit_flag = True


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    fileDir = filedialog.askdirectory()
    print(fileDir)
    main(fileDir)



    
