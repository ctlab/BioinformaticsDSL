from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5 import QtGui, QtCore


class StepArgsModel(QtCore.QAbstractItemModel):
    def __init__(self, step):
        QtCore.QAbstractItemModel.__init__(self)
        self._step = step

    def rowCount(self, in_index):
        return len(self._step._inputs) + len(self._step._outputs)

    def columnCount(self, in_index):
        return 4

    def index(self, in_row, in_column, in_parent=None):
        return QtCore.QAbstractItemModel.createIndex(self, in_row, in_column)

    def data(self, in_index, role):
        if not in_index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            key = ['io', 'name', 'type', 'value'][in_index.column()]
            return self._step._args[in_index.row()][key]

    def flags(self, in_index):
        if not in_index.isValid():
            return None

        if in_index.column() == 3:
            return super().flags(in_index) | QtCore.Qt.ItemIsEditable
        else:
            return super().flags(in_index)

    def setData(self, in_index, in_data, role):
        if not in_index.isValid():
            return False

        if in_index.column() == 3:
            self._step._args[in_index.row()]['value'] = in_data
            return True

        return False

    def headerData(self, id, orient, role=None):
        if orient != QtCore.Qt.Horizontal or role != QtCore.Qt.DisplayRole:
            return None

        return ['io', 'name', 'type', 'value'][id]


class Step(QFrame):

    selected = QtCore.pyqtSignal()

    def __init__(self, name, args, parent=None):
        QFrame.__init__(self, parent)
        self._model = StepArgsModel(self)
        self._args = args
        self._name = name

        self._offset = QtCore.QPoint()
        self._inputs = {}
        self._outputs = {}
        self._selected = False

        self.inut_ui(name, args)
        self._set_style()

    def _set_style(self):
        self.setStyleSheet('Step { background-color: lightgray; border:%dpx solid %s; }' % ((3, 'red') if self._selected else (1, 'black')))

    def inut_ui(self, name, args):
        vl = QVBoxLayout()
        lbl = QLabel(self)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        lbl.setText(name)
        vl.addWidget(lbl)
        hl = QHBoxLayout()
        il = QVBoxLayout()
        il.setAlignment(QtCore.Qt.AlignTop)
        for arg in args:
            if arg['io'] == 'i':
                inp_lbl = QLabel(self)
                self._inputs[arg['name']] = inp_lbl
                inp_lbl.setText(arg['name'])

                il.addWidget(inp_lbl)
        ol = QVBoxLayout()
        ol.setAlignment(QtCore.Qt.AlignTop)
        for arg in args:
            if arg['io'] == 'o':
                out_lbl = QLabel(self)
                self._outputs[arg['name']] = out_lbl
                out_lbl.setAlignment(QtCore.Qt.AlignRight)
                out_lbl.setText(arg['name'])
                ol.addWidget(out_lbl)
        hl.addLayout(il)
        hl.addLayout(ol)
        vl.addLayout(hl)
        self.setLayout(vl)

    def mousePressEvent(self, event):
        self._offset = event.pos()
        self.selected.emit()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.move(self.mapToParent(event.pos() - self._offset))
            QFrame.parent(self).repaint()

    def get_connect_pos(self, name):
        if name in self._inputs:
            return self.mapToParent(self._inputs[name].geometry().topLeft() + QtCore.QPoint(0, self._inputs[name].height() / 2))
        if name in self._outputs:
            return self.mapToParent(self._outputs[name].geometry().topRight() + QtCore.QPoint(0, self._outputs[name].height() / 2))

    def select(self, selected):
        self._selected = selected
        self._set_style()

    def get_name(self):
        return self._name

    def get_args_model(self):
        return self._model

    def get_inputs_names(self):
        return [arg['name'] for arg in self._args if arg['io'] == 'i']

    def get_outputs_names(self):
        return [arg['name'] for arg in self._args if arg['io'] == 'o']