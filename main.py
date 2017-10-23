import sys
import threading

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from plotting import MyDynamicMplCanvas
from Interpreter import Interpreter, Variables

def main():

    app = QtWidgets.QApplication(sys.argv)

    # set up main display window

    display = ApplicationWindow()
    display.show()

    sys.exit(app.exec_())


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.main_widget = QtWidgets.QWidget(self)
        l = QtWidgets.QHBoxLayout(self.main_widget)

        interp = Interpreter(self.main_widget)
        l.addWidget(interp)

        self.tree_widget = Variables(self.main_widget, interp.session)
        l.addWidget(self.tree_widget)
        interp.textChanged.connect(self.tree_widget.get_items)

        dynamic = MyDynamicMplCanvas()
        l.addWidget(dynamic)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)


if __name__ == '__main__':
    main()
