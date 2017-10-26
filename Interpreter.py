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
        self.locals = {'parent':master.parent(), '__builtins__':__builtins__}
        self.globals = {}
        self.history = []
        self.history_idx = 0

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
                self.history.append(cmd)
                self.history_idx = 0

            except Exception as e:
                self.out.write(e)
            finally:
                self.out.close()
                self.blockSignals(False)

    def keyPressEvent(self, e):
        # TODO implement history
        if e.key() == QtCore.Qt.Key_Up:
            self.history_idx -= 1
            msg = self.history[self.history_idx] if self.history_idx < 0 else ''
            self.out.write(msg)
        elif e.key() == QtCore.Qt.Key_Down:
            self.history_idx += 1
            msg = self.history[self.history_idx] if self.history_idx < 0 else ''
            self.out.write(msg)
        else:
            QtWidgets.QPlainTextEdit.keyPressEvent(self, e)


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
