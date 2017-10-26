import sys
import threading

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from plotting import FTPlot
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
        self.setup_ui()

    def setup_ui(self):

        self.main_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QHBoxLayout(self.main_widget)

        self.interp = Interpreter(self.main_widget)
        self.layout.addWidget(self.interp)

        self.tree_widget = Variables(self.main_widget)
        self.layout.addWidget(self.tree_widget)

        # connect slots and fire signal once so that builtins appear
        self.interp.variables.connect(self.tree_widget.get_items)
        self.interp.variables.emit(self.interp.locals)

        # set focus and main widget
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def plot(self, *args, **kwargs):
        self.dynamic = FTPlot(self.main_widget)
        self.layout.addWidget(self.dynamic)
        self.dynamic.plot(*args, **kwargs)

if __name__ == '__main__':
    main()
