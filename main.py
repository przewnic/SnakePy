# Author: przewnic
""" Snake game app. """

import sys
from PyQt5 import QtWidgets
from MainWindow import MainWindow


def main():
    """ Start the app loop. """
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
