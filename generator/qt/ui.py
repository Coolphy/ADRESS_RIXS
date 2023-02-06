# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerkoQdDi.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import sys

from PyQt5.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QHeaderView,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)

import scripts_generator as sg


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 900)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QTableWidget(self.centralwidget)
        if self.tableWidget.columnCount() < 11:
            self.tableWidget.setColumnCount(11)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        if self.tableWidget.rowCount() < 1:
            self.tableWidget.setRowCount(1)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem11)
        self.tableWidget.setObjectName("tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")

        self.verticalLayout.addWidget(self.pushButton_3)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.connect_slots()

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Script Generator", None)
        )
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("MainWindow", "PhotonEnergy", None)
        )
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate("MainWindow", "PolarMode", None)
        )
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate("MainWindow", "SampleXs", None)
        )
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("MainWindow", "SampleYs", None)
        )
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate("MainWindow", "SampleZ", None)
        )
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate("MainWindow", "SampleTheta", None)
        )
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate("MainWindow", "SamplePhi", None)
        )
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem6.setText(
            QCoreApplication.translate("MainWindow", "SampleTilt", None)
        )
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem7.setText(
            QCoreApplication.translate("MainWindow", "AcquireTime", None)
        )
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem8.setText(
            QCoreApplication.translate("MainWindow", "ExposureSplit", None)
        )
        # ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(10)
        # ___qtablewidgetitem9.setText(
        #     QCoreApplication.translate("MainWindow", "ExitSlit", None)
        # )
        ___qtablewidgetitem10 = self.tableWidget.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(
            QCoreApplication.translate("MainWindow", "Repeat", None)
        )
        ___qtablewidgetitem11 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem11.setText(
            QCoreApplication.translate("MainWindow", "1", None)
        )
        self.pushButton.setText(
            QCoreApplication.translate("MainWindow", "Insert Row", None)
        )
        self.pushButton_2.setText(
            QCoreApplication.translate("MainWindow", "Remove Row", None)
        )
        self.pushButton_3.setText(
            QCoreApplication.translate("MainWindow", "Generate !", None)
        )

    def connect_slots(self):
        self.pushButton.clicked.connect(self.do_insert)
        self.pushButton_2.clicked.connect(self.do_remove)
        self.pushButton_3.clicked.connect(self.do_generate)

    def do_insert(self):
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)

    def do_remove(self):
        rowCount = self.tableWidget.rowCount()
        if rowCount > 1:
            self.tableWidget.removeRow(rowCount - 1)

    def load_row(self, row):
        status = {}
        strings = [
            "energy",
            "polar",
            "samx",
            "samy",
            "samz",
            "samt",
            "phi",
            "tilt",
            "exposure",
            "split",
            "acquire",
        ]

        for column in range(11):
            status[strings[column]] = (
                float(self.tableWidget.item(row, column).text())
                if self.tableWidget.item(row, column) is not None
                else None
            )

        return status

    def load_status(self):
        status = {}
        for row in range(self.tableWidget.rowCount()):
            status[row] = self.load_row(row)
            for key in status[row]:
                if (row != 0) & (status[row][key] == None):
                    status[row][key] = status[row - 1][key]
        return status

    def do_generate(self):

        status = self.load_status()
        # print(status)

        sg.init()
        sg.load(status)
        command_string = sg.fprint(1)

        savefile, _ = QFileDialog.getSaveFileName(
            directory="Untitle.txt", filter="Text (*.txt)"
        )
        if savefile == "":
            pass
        else:
            with open(savefile, "w") as f:
                f.write(command_string)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
