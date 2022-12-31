import sys
import os

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import pyqtgraph as pg

import h5py
import numpy as np

from mda_utils.load_mda import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listView")

        self.verticalLayout.addWidget(self.listWidget)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.graphWidget = pg.PlotWidget(self.centralwidget)
        self.graphWidget.setObjectName("graphWidget")

        self.gridLayout.addWidget(self.graphWidget, 0, 0, 1, 1)
        self.graphWidget.setBackground("w")
        self.graphWidget.getAxis("left").setTextPen("black")
        self.graphWidget.getAxis("bottom").setTextPen("black")
        self.graphWidget.plotItem.getViewBox().setMouseMode(pg.ViewBox.RectMode)

        self.horizontalLayout_2.addLayout(self.gridLayout)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 5)

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)

        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        self.connect_slots()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MDAViewer", None)
        )
        self.pushButton_2.setText(
            QCoreApplication.translate("MainWindow", "Save", None)
        )
        self.pushButton.setText(QCoreApplication.translate("MainWindow", "Open", None))

    def connect_slots(self):
        self.pushButton.clicked.connect(self.button_clicked)
        self.lineEdit.editingFinished.connect(self.line_edit_finish)
        self.pushButton_2.clicked.connect(self.button_2_clicked)
        self.listWidget.itemClicked.connect(self.listWidget_clicked)
        self.listWidget.itemDoubleClicked.connect(self.listWidget_double_clicked)

    def button_clicked(self):
        self.path = QFileDialog.getExistingDirectory()
        self.lineEdit.setText(self.path)
        self.listWidget.clear()
        list = sorted(os.listdir(self.path))
        self.listWidget.addItems(list)

    def line_edit_finish(self):
        self.path = self.lineEdit.text()
        self.listWidget.clear()
        list = sorted(os.listdir(self.path))
        self.listWidget.addItems(list)

    def button_2_clicked(self):

        if self.mda is not None:
            savefile, _ = QFileDialog.getSaveFileName(
                dir=f"{self.path}/{self.filename[:-4]}", filter="Text (*.txt)"
            )
            if savefile == "":
                pass
            else:
                self.mda.save(savefile[:-4])

    def listWidget_clicked(self, item):
        self.filename = item.text()
        self.mda = load_mda()
        self.mda.load(f"{self.path}/{self.filename}")
        self.plot()

    def listWidget_double_clicked(self):
        return

    def plot(self):

        self.graphWidget.clear()

        # styles = {"color": "b", "font-size": "10px"}
        # self.graphWidget.setLabel("left", "Counts", **styles)
        # self.graphWidget.setLabel("bottom", "pixel", **styles)
        # Add legend
        self.graphWidget.addLegend(labelTextColor="black")
        # Add grid
        # self.graphWidget.showGrid(x=True, y=True)
        # Set Range
        # self.graphWidget.setXRange(0, 6000, padding=0)
        # self.graphWidget.setYRange(0, 100, padding=0)

        color = [
            "#0072BD",
            "#D95319",
            "#EDB120",
            "#7E2F8E",
            "#77AC30",
            "#4DBEEE",
            "#A2142F",
        ]

        if self.mda.data["dimension"] == 1:

            for i, d in enumerate(self.mda.data["detectors"]):

                pen = pg.mkPen(color[i])
                self.graphWidget.plot(
                    self.mda.data["positioners"][0]["data"],
                    self.mda.data["detectors"][d]["data"],
                    name=f"d{i}",
                    pen=pen,
                )

        elif self.mda.data["dimension"] == 2:
            pen = pg.mkPen(color[0])
            self.graphWidget.plot(
                [0],
                [0],
                name="2-D data",
                pen=pen,
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
