import sys

from h5py import File
import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=6.4, height=4.8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # matplotlib canvas
        self.canvas = MplCanvas(self, width=6.4, height=4.8, dpi=100)
        self.setCentralWidget(self.canvas)

        # load data
    def load_data(self, filename):
        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]

    def plot_rixs(self):
        self.update_plot(self)
        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def watch_file(self,filename):
        self.filename = filename

    def update_plot(self):
 
        # filename = adress_tools.make_filename(self,filepath,base_atom,runNB)
        self.ydata,self.ydata = adress_tools.load_data(self,self.filename)
        self.canvas.axes.cla()
        self.canvas.axes.plot(self.xdata, self.ydata)
        self.canvas.draw()

class adress_tools:

    def __init__(self) -> None:
        pass

    def make_filename(self,filepath,base_atom,runNB):
        filename = filepath + base_atom + '_{:.4d}'.format(runNB) + '.h5'
        return filename

    def load_data(self,filename):
        self.f = File(filename, "r")
        ydata = self.f["entry"]["analysis"]["spectrum"][()]
        xdata = np.arange(len(ydata))
        return xdata,ydata

    def load_meta(self):
        meta_data = self.f["entry"]["NDAttribute"]
        return meta_data



app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()