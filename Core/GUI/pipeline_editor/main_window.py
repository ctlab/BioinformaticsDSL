import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
from GUI.pipeline_editor.main_window_ui import Ui_MainWindow
from GUI.pipeline_editor.work_area import WorkArea
from package_manager import PackageManager
import xml.etree.ElementTree as ET

class PackagesModel(QtCore.QAbstractListModel):
    def __init__(self, pm):
        super(QtCore.QAbstractListModel, self).__init__()
        self._pm = pm

    def rowCount(self, in_index):
        return len(self._pm.get_pl_list())

    def index(self, in_row, in_column, in_parent=None):
        return QtCore.QAbstractListModel.createIndex(self, in_row, 0)

    def data(self, in_index, role):
        if not in_index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            return '/'.join(self._pm.get_pl_list()[in_index.row()])

        if role == QtCore.Qt.UserRole:
            return self._pm.get_pl_list()[in_index.row()]

class MainWindow(Ui_MainWindow):
    def __init__(self, parent):
        self.setupUi(parent)
        self._last_step_id = 0
        self._work_area = WorkArea(self.centralwidget)

        self.init_package_model()
        self.areaLayout.addWidget(self._work_area)
        self.connect_slots()

    def init_package_model(self):
        self._pm = PackageManager('/home/fedor/DSL/BioinformaticsDSL/Utils')
        self._packages_model = PackagesModel(self._pm)
        self._filter_model = QtCore.QSortFilterProxyModel()
        self._filter_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._filter_model.setSourceModel(self._packages_model)
        self.lstTools.setModel(self._filter_model)


    def connect_slots(self):
        self.edFilter.textChanged.connect(self.filter_chainged)
        self.btnAddStep.clicked.connect(self.add_step)
        self.btnConnect.clicked.connect(self.connect_steps)

    def filter_chainged(self, text):
        self._filter_model.setFilterRegExp(QtCore.QRegExp(text))

    def _get_pl_info(self, pl_path):
        inputs, outputs = [], []
        root = ET.parse(pl_path).getroot()
        for child in root:
            if child.tag == 'input':
                inputs.append(child.attrib['name'])
            if child.tag == 'output':
                outputs.append(child.attrib['name'])

        return inputs, outputs



    def add_step(self):
        self._last_step_id += 1
        step_name = "step_%d" % self._last_step_id
        idx = self.lstTools.selectionModel().currentIndex()
        data = self._filter_model.data(idx, QtCore.Qt.UserRole)
        pl_path = self._pm.find_pipeline(*data)
        inputs, outputs = self._get_pl_info(pl_path)
        self._work_area.add_step(step_name, inputs, outputs)


    def connect_steps(self):

        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = MainWindow(window)
    window.show()
    sys.exit(app.exec_())