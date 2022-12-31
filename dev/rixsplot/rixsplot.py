# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uieVoYJS.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import sys
import os

import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

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


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QWidget()
        self.tab_1.setObjectName("tab_1")
        self.gridLayout_4 = QGridLayout(self.tab_1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QListWidget(self.tab_1)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )

        self.verticalLayout.addWidget(self.listWidget)

        self.pushButton_2 = QPushButton(self.tab_1)
        self.pushButton_2.setObjectName("pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_3 = QPushButton(self.tab_2)
        self.pushButton_3.setObjectName("pushButton_3")

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.tab_2)
        self.pushButton_4.setObjectName("pushButton_4")

        self.verticalLayout_2.addWidget(self.pushButton_4)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label = QLabel(self.tab_2)
        self.label.setObjectName("label")

        self.verticalLayout_2.addWidget(self.label)

        self.lineEdit_2 = QLineEdit(self.tab_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setText("0")

        self.verticalLayout_2.addWidget(self.lineEdit_2)

        self.pushButton_5 = QPushButton(self.tab_2)
        self.pushButton_5.setObjectName("pushButton_5")

        self.verticalLayout_2.addWidget(self.pushButton_5)

        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.lineEdit_3 = QLineEdit(self.tab_2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setText("1")

        self.verticalLayout_2.addWidget(self.lineEdit_3)

        self.pushButton_6 = QPushButton(self.tab_2)
        self.pushButton_6.setObjectName("pushButton_6")

        self.verticalLayout_2.addWidget(self.pushButton_6)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.pushButton_7 = QPushButton(self.tab_2)
        self.pushButton_7.setObjectName("pushButton_7")

        self.verticalLayout_2.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.tab_2)
        self.pushButton_8.setObjectName("pushButton_8")

        self.verticalLayout_2.addWidget(self.pushButton_8)

        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_3 = QGridLayout(self.tab_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.mplCanvas = MplCanvas(self)
        self.mplCanvas.setObjectName("mplCanvas")
        self.mplToolbar = NavigationToolbar(self.mplCanvas, MainWindow)
        self.mplToolbar.setObjectName("mplToolbar")

        self.verticalLayout_3.addWidget(self.mplToolbar)
        self.verticalLayout_3.addWidget(self.mplCanvas)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_5 = QGridLayout(self.tab_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tableWidget = QTableWidget(self.tab_4)
        self.tableWidget.setObjectName("tableWidget")

        self.gridLayout_5.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_4, "")

        self.horizontalLayout_2.addWidget(self.tabWidget_2)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)

        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.connectUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "RIXSplot", None)
        )
        self.pushButton.setText(QCoreApplication.translate("MainWindow", "Open", None))
        self.pushButton_2.setText(
            QCoreApplication.translate("MainWindow", "Plot", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_1),
            QCoreApplication.translate("MainWindow", "Files", None),
        )
        self.pushButton_3.setText(
            QCoreApplication.translate("MainWindow", "Xcorr", None)
        )
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", "Sum", None))
        self.label.setText(QCoreApplication.translate("MainWindow", "Zero", None))
        self.pushButton_5.setText(
            QCoreApplication.translate("MainWindow", "Shift", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", "Dispersion", None)
        )
        self.pushButton_6.setText(
            QCoreApplication.translate("MainWindow", "Etrans", None)
        )
        self.pushButton_7.setText(
            QCoreApplication.translate("MainWindow", "Peak", None)
        )
        self.pushButton_8.setText(
            QCoreApplication.translate("MainWindow", "Save", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            QCoreApplication.translate("MainWindow", "Process", None),
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_3),
            QCoreApplication.translate("MainWindow", "Spectrum", None),
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_4),
            QCoreApplication.translate("MainWindow", "Info", None),
        )

    def connectUi(self, MainWindow):
        self.pushButton.clicked.connect(self.do_open)
        self.lineEdit.editingFinished.connect(self.lineEdit_finish)
        self.pushButton_2.clicked.connect(self.do_plot)
        self.pushButton_3.clicked.connect(self.do_correlate)
        self.pushButton_4.clicked.connect(self.do_sum)
        self.pushButton_5.clicked.connect(self.do_shift)
        self.pushButton_6.clicked.connect(self.do_etrans)

        self.pushButton_8.clicked.connect(self.do_save)

        self.mplCanvas.mpl_connect("button_press_event", self.mpl_on_click)

    def do_open(self):
        self.path = QFileDialog.getExistingDirectory()
        self.lineEdit.setText(self.path)
        self.listWidget.clear()
        list = sorted(os.listdir(self.path))
        self.listWidget.addItems(list)

    def lineEdit_finish(self):
        self.path = self.lineEdit.text()
        self.listWidget.clear()
        list = sorted(os.listdir(self.path))
        self.listWidget.addItems(list)

    def do_plot(self):
        self.items = self.listWidget.selectedItems()
        self.data = {}
        self.rt = rixs_tools()
        for item in self.items:
            self.data[item.text()] = self.rt.load_ccd(f"{self.path}/{item.text()}")
        self.plot_multi_lines(self.data)
        self.mplCanvas.axes.set_xlabel("Pixels")
        self.mplCanvas.axes.set_ylabel("Counts")
        self.mplCanvas.draw()

    def do_correlate(self):
        xrange = self.mplCanvas.axes.get_xlim()
        yrange = self.mplCanvas.axes.get_ylim()
        for i, item in enumerate(self.items):
            if i == 0:
                refdata = self.data[item.text()]
            else:
                tempdata = self.data[item.text()]
                self.data[item.text()] = self.rt.x_corr(
                    refdata, tempdata, xrange=xrange
                )
        self.plot_multi_lines(self.data)
        self.mplCanvas.axes.set_xlim(xrange)
        self.mplCanvas.axes.set_ylim(yrange)
        self.mplCanvas.axes.set_xlabel("Pixels")
        self.mplCanvas.axes.set_ylabel("Counts")
        self.mplCanvas.draw()

    def do_sum(self):
        for i, key in enumerate(self.data):
            if i == 0:
                self.ydata = self.data[key]
            else:
                self.ydata = self.ydata + self.data[key]
        self.xdata = np.arange(len(self.ydata))
        self.plot_one_line(self.xdata, self.ydata)
        self.mplCanvas.axes.set_xlabel("Pixels")
        self.mplCanvas.axes.set_ylabel("Counts")
        self.mplCanvas.draw()

    def do_shift(self):
        shifts = float(self.lineEdit_2.text())
        self.xdata = self.xdata - shifts
        self.plot_one_line(self.xdata, self.ydata)
        self.mplCanvas.axes.set_xlabel("Pixel Transfer")
        self.mplCanvas.axes.set_ylabel("Counts")
        self.mplCanvas.draw()

    def do_etrans(self):
        dispersion = float(self.lineEdit_3.text())
        self.xdata = self.xdata * dispersion
        self.plot_one_line(self.xdata, self.ydata)
        self.mplCanvas.axes.set_xlabel("Energy Transfer")
        self.mplCanvas.axes.set_ylabel("Counts")
        self.mplCanvas.draw()

    def do_save(self):
        if self.ydata is not None:
            savefile, _ = QFileDialog.getSaveFileName(dir=f"", filter="Text (*.txt)")
            if savefile == "":
                pass
            else:
                data = np.array([self.xdata, self.ydata])
                np.savetxt(
                    savefile,
                    np.transpose(data),
                    delimiter="\t",
                    header="Energy\tCounts",
                    comments="#",
                )

    def plot_one_line(self, xdata, ydata):
        self.mplCanvas.axes.cla()
        self.mplCanvas.axes.plot(xdata, ydata, lw=0.5)
        self.mplCanvas.draw()

    def plot_multi_lines(self, data):
        self.mplCanvas.axes.cla()
        for key in data:
            self.mplCanvas.axes.plot(data[key], lw=0.5)
        self.mplCanvas.draw()

    def mpl_on_click(self, event):
        ix, iy = event.xdata, event.ydata
        self.lineEdit_2.setText(f"{ix:.4f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
