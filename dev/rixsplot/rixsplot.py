import sys

from PySide6.QtCore import (
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
from PySide6.QtGui import (
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
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)
import pyqtgraph as pg


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

        self.verticalLayout_2.addWidget(self.lineEdit_2)

        self.pushButton_5 = QPushButton(self.tab_2)
        self.pushButton_5.setObjectName("pushButton_5")

        self.verticalLayout_2.addWidget(self.pushButton_5)

        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.lineEdit_3 = QLineEdit(self.tab_2)
        self.lineEdit_3.setObjectName("lineEdit_3")

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
        self.gridLayout_6 = QGridLayout(self.tab_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.graphWidget = pg.PlotWidget(self.tab_3)
        self.graphWidget.setObjectName("graphWidget")

        self.gridLayout_6.addWidget(self.graphWidget, 0, 0, 1, 1)

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

        self.tabWidget.setCurrentIndex(1)
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
            QCoreApplication.translate("MainWindow", "More", None),
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_3),
            QCoreApplication.translate("MainWindow", "Plot", None),
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_4),
            QCoreApplication.translate("MainWindow", "Info", None),
        )

    # retranslateUi


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
