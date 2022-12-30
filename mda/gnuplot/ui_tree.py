import sys
from os import path

# from mda import *
from load_mda import *

# import numpy as np

# from PySide6.QtGui import *
from PySide6.QtWidgets import QTreeView, QApplication, QFileSystemModel

# import subprocess
from gnuplot import *


class Tree(QTreeView):
    def __init__(self, parent=None):
        super(Tree, self).__init__(parent)

        path = "X:/"
        self.model = QFileSystemModel()
        self.model.setRootPath(path)

        self.setModel(self.model)
        self.setWindowTitle("MDA viewer")
        self.resize(640, 480)

        self.setRootIndex(self.model.index(path))
        self.doubleClicked.connect(self.double_click_success)

    def double_click_success(self, Qmodelidx):
        filePath = self.model.filePath(Qmodelidx)
        fileName = self.model.fileName(Qmodelidx)

        s = load_mda()
        s.load_data(filePath)
        s.save_data(f"{filePath}.txt")
        [xlabel, ylabel] = s.header.split(",")[0:2]

        if path.exists("C:/Program Files/gnuplot/bin/gnuplot.exe"):
            gnu_path = "C:/Program Files/gnuplot/bin/gnuplot.exe"
        elif path.exists("C:/Tools/gnuplot/bin/gnuplot.exe"):
            gnu_path = "C:/Tools/gnuplot/bin/gnuplot.exe"
        else:
            gnu_path = "gnuplot"

        try:
            gp = gnuplot(gnu_path)
            if s.rank == 1:
                cmd_arg = f'plot "{filePath}.txt" u 1:2 w l'
            if s.rank == 2:
                cmd_arg = f'set pm3d\nset hidden3d\nset pm3d map\nset size square\nset palette rgbformulae 22, 13, -31\nsplot "{filePath}.txt" w l\n'
            gp.set_label(xlabel, ylabel)
            gp.set_title(fileName)
            gp.run_command(cmd_arg)
            gp.draw()
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tree = Tree()
    tree.show()
    sys.exit(app.exec())
