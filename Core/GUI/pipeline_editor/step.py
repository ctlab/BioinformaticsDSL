from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5 import QtGui, QtCore


class Step(QFrame):
    def __init__(self, name, inputs, outputs, parent=None):
        super(Step, self).__init__(parent)
        self._offset = QtCore.QPoint()
        self._inputs = {}
        self._outputs = {}

        vl = QVBoxLayout()
        lbl = QLabel(self)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        lbl.setText(name)
        vl.addWidget(lbl)

        hl = QHBoxLayout()

        il = QVBoxLayout()
        il.setAlignment(QtCore.Qt.AlignTop)
        for input in inputs:
            inp_lbl = QLabel(self)
            self._inputs[input] = inp_lbl
            inp_lbl.setText(input)
            il.addWidget(inp_lbl)

        ol = QVBoxLayout()
        ol.setAlignment(QtCore.Qt.AlignTop)
        for output in outputs:
            out_lbl = QLabel(self)
            self._outputs[output] = out_lbl
            out_lbl.setAlignment(QtCore.Qt.AlignRight)
            out_lbl.setText(output)
            ol.addWidget(out_lbl)

        hl.addLayout(il)
        hl.addLayout(ol)
        vl.addLayout(hl)

        self.setLayout(vl)
        self.setStyleSheet("Step { background-color: lightgray; border:1px solid black; }")

    def mousePressEvent(self, event):
        self._offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.move(self.mapToParent(event.pos() - self._offset))
            self.parent().repaint()

    def get_connect_pos(self, name):
        if name in self._inputs:
            return self.mapToParent(self._inputs[name].geometry().topLeft() + QtCore.QPoint(0, self._inputs[name].height() / 2))
        if name in self._outputs:
            return self.mapToParent(self._outputs[name].geometry().topRight() + QtCore.QPoint(0, self._outputs[name].height() / 2))

