from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class FTPlot(QtWidgets.QWidget):
    def __init__(self, parent, dpi=100):
        QtWidgets.QWidget.__init__(self, parent)

        self.fig = Figure((5.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        #self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.mpl_toolbar)
        self.setLayout(vbox)

        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        self.canvas.updateGeometry()

    def plot(self, *args, **kwargs):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.plot(*args, **kwargs)
        self.canvas.draw()
