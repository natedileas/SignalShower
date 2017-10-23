import code
import os
import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore

class Out(object):
    def __init__(self, outfunc):
        self.outfunc = outfunc
        self._stdout = None
    def write(self, stuff, ps1=True):
        self.outfunc(str(stuff))
    def flush(self):
        pass
    def open(self):
        if not self._stdout:
            self._stdout = sys.stdout
            self._stderr = sys.stderr
            sys.stdout = self
            sys.stderr = self
    def close(self):
        if self._stdout:
            sys.stdout = self._stdout
            sys.stderr = self._stderr
            self._stdout = None
            self._stderr = None

class Interpreter(QtWidgets.QPlainTextEdit):
    ps1 = '>>> '
    ps2 = '... '
    linesep = '\n'
    variables = QtCore.pyqtSignal(dict)

    def __init__(self, master):
        QtWidgets.QPlainTextEdit.__init__(self, master)
        self.locals = {}
        self.globals = {}

        self.textChanged.connect(self.changed)
        self.out = Out(self.insertPlainText)
        self.out.write(self.ps1)

        self.interp = code.InteractiveInterpreter(self.locals)


    @QtCore.pyqtSlot()
    def changed(self):
        text = self.toPlainText()

        if text[-1] == self.linesep:
            try:
                self.blockSignals(True)
                self.out.open()

                # strip trailing newline and remove sub prompt
                cmd = text.split(self.ps1)[-1].rstrip(self.linesep)
                cmd = cmd.replace(self.ps2, "")

                ret = self.interp.runsource(cmd)
                if ret:
                    self.out.write(self.ps2)
                else:
                    self.out.write(self.ps1)

                self.blockSignals(False)
                self.variables.emit(self.locals)

            except Exception as e:
                self.out.write(e)
            finally:
                self.out.close()
                self.blockSignals(False)


class Variables(QtWidgets.QTreeWidget):
    def __init__(self, master):
        QtWidgets.QTreeWidget.__init__(self, master)
        self.setColumnCount(3)
        self.setHeaderLabels(['Variable', 'Type', 'Value'])

    @QtCore.pyqtSlot(dict)
    def get_items(self, obj):
        items = []
        for key in obj:
            val = obj[key]
            items.append(QtWidgets.QTreeWidgetItem([str(key), str(type(val)),
                        'Len: '+str(len(val)) if type(val) is list else str(val)]))
        self.clear()
        self.insertTopLevelItems(0, items)
