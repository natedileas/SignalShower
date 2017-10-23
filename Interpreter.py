import code
import os
import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore

class Session(object):
    def clear(self):
        self.__dict__ = {}

class Out:
    def __init__(self, outfunc):
        self.outfunc = outfunc
        self.buffer = ''
        self._stdout = None
    def write(self, stuff, ps1=True):
        if ps1:
            self.outfunc(str(stuff))
        else:
            self.outfunc(str(stuff))
    def flush(self):
        pass
    def open(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self
    def close(self):
        if self._stdout:
            sys.stdout = self._stdout
            sys.stderr = self._stderr

class Interpreter(QtWidgets.QPlainTextEdit):
    ps1 = '>>> '
    ps2 = '... '
    linesep = '\n'

    def __init__(self, master):
        QtWidgets.QTextEdit.__init__(self, master)
        #elf.setAcceptRichText(False)

        self.session = Session()

        self.textChanged.connect(self.changed)
        self.insertPlainText(self.ps1)
        self.out = Out(self.insertPlainText)

        self.interp= code.InteractiveInterpreter(self.session.__dict__)

    @QtCore.pyqtSlot()
    def changed(self):

        text = self.toPlainText()

        if text[-1] == self.linesep:
            try:
                self.out.open()

                # strip trailing newline and remove sub prompt
                cmd = text.split(self.ps1)[-1].rstrip(self.linesep)
                #cmd = cmd.replace(self.ps2, "")

                if len(cmd) < 1:
                    self.out.write('')
                    return

                ret = self.interp.runsource(cmd)
                if ret:
                    self.out.write(self.ps2)
                else:
                    self.out.write(self.ps1)

                #codeobj = code.compile_command(cmd, filename="<input>", symbol='single')
                #if not codeobj:   # command is incomplete
                #    self.out.write(self.ps2, False)
                #    return
                #exec(codeobj, self.session.__dict__, self.session.__dict__)
                #self.out.write(ret)
            except Exception as e:
                self.out.write(e)
            finally:
                self.out.close()



class Variables(QtWidgets.QTreeWidget):
    def __init__(self, master, obj):
        QtWidgets.QTreeWidget.__init__(self, master)
        self.obj = obj
        self.setColumnCount(3)
        self.setHeaderLabels(['Variable', 'Type', 'Value'])
        self.insertTopLevelItems(0, self.get_items())

    @QtCore.pyqtSlot()
    def get_items(self):
        items = []
        for key in vars(self.obj):
            val = vars(self.obj)[key]
            items.append(QtWidgets.QTreeWidgetItem([str(key), str(type(val)),
                        'Len: '+str(len(val)) if type(val) is list else str(val)]))

        return items
