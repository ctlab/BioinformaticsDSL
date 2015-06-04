from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui, QtCore
from GUI.pipeline_editor.step import Step

class WorkArea(QWidget):
    def __init__(self, parent=None):
        super(WorkArea, self).__init__(parent)
        self._steps = []
        self._last_step_pos = QtCore.QPoint(100, 100)
        self._step_size = QtCore.QSize(150, 100)

        self.add_step('step 1', ['i1', 'i2'], ['o1', 'o2', 'o3'])
        self.add_step('step 2', ['i1', 'i2'], ['o1', 'o2', 'o3'])


    def add_step(self, name, inputs, outputs):
        st = Step(name, inputs, outputs, self)
        self._last_step_pos += QtCore.QPoint(50, 50)
        st.setGeometry(QtCore.QRect(self._last_step_pos, self._step_size))
        self._steps.append(st)


    def paintEvent(self, event = None):
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        paint.setPen(QtGui.QPen(QtGui.QColor(QtCore.Qt.red)))
        paint.fillRect(self.rect(), QtCore.Qt.white)

        #paint.drawLine(self._steps[0].get_connect_pos(), self._steps[1].get_connect_pos())
        paint.end()