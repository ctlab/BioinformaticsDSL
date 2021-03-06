from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5 import QtGui, QtCore
from GUI.pipeline_editor.step import Step

class WorkArea(QWidget):

    params_chainged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WorkArea, self).__init__(parent)
        self._steps = []
        self._connections = []
        self._last_step_pos = QtCore.QPoint(100, 100)
        self._selected_step = None
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self._inputs = None
        self._outputs = None

    def _set_step_geometry(self, step, args):
        ih = len([arg for arg in args if arg['io'] == 'i']) * 25
        oh = len([arg for arg in args if arg['io'] == 'o']) * 25
        step_size = QtCore.QSize(100 if ih * oh == 0 else 200, max(ih, oh) + 25)
        step.setGeometry(QtCore.QRect(self._last_step_pos, step_size))

    def add_step(self, name, args):
        st = Step(name, args, self)
        st.selected.connect(self.step_selected)
        self._last_step_pos += QtCore.QPoint(50, 50)
        self._set_step_geometry(st, args)
        self._steps.append(st)
        st.show()

    def set_inputs(self, args):
        if self._inputs is not None:
            self._inputs.deleteLater()
        st = Step('inputs', args, self)
        st.selected.connect(self.step_selected)
        self._last_step_pos += QtCore.QPoint(50, 50)
        self._set_step_geometry(st, args)
        self._inputs = st
        self._steps.append(st)
        st.show()

    def set_outputs(self, args):
        if self._outputs is not None:
            self._outputs.deleteLater()
        st = Step('outputs', args, self)
        st.selected.connect(self.step_selected)
        self._last_step_pos += QtCore.QPoint(50, 50)
        self._set_step_geometry(st, args)
        self._outputs = st
        self._steps.append(st)
        st.show()

    def remove_step(self):
        step = self.get_selected_step()
        if self._inputs == step or self._outputs == step:
            return
        if step is not None:
            self._steps.remove(step)
            self._connections = [conn for conn in self._connections if (conn[0] != step and conn[2] != step)]
            step.deleteLater()
            self.repaint()


    def connect_steps(self, step_from, output, step_to, input):
        self._connections.append((step_from, output, step_to, input))
        self.repaint()

    def _draw_connection(self, paint, f, t):
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        paint.setPen(QtGui.QPen(QtGui.QColor(QtCore.Qt.red)))
        paint.drawLine(f, t)

    def paintEvent(self, event = None):
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.fillRect(self.rect(), QtCore.Qt.white)

        for conn in self._connections:
            self._draw_connection(paint, conn[0].get_connect_pos(conn[1]), conn[2].get_connect_pos(conn[3]))
        paint.end()

    def add_to_pl(self, pl):
        pass

    def step_selected(self):
        self._selected_step = self.sender()
        for step in self._steps:
            step.select(step == self._selected_step)

        self.params_chainged.emit()

    def get_selected_step(self):
        return self._selected_step

    def get_steps_names(self):
        return [step.get_name() for step in self._steps]

    def find_step(self, name):
        for step in self._steps:
            if step.get_name() == name:
                return step
        return None

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.remove_step()
        else:
            super(WorkArea, self).keyPressEvent(event)







