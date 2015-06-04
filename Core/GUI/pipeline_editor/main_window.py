import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
from GUI.pipeline_editor.main_window_ui import Ui_MainWindow
from GUI.pipeline_editor.work_area import WorkArea
from package_manager import PackageManager

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

class MainWindow(Ui_MainWindow):
    def __init__(self, parent):
        self.setupUi(parent)
        self._work_area = WorkArea(self.centralwidget)

        self.init_package_model()
        self.areaLayout.addWidget(self._work_area)
        self.connect_slots()

    def init_package_model(self):
        self._packages_model = PackagesModel(PackageManager('/home/fedor/DSL/BioinformaticsDSL/Utils'))
        self._filter_model = QtCore.QSortFilterProxyModel()
        self._filter_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._filter_model.setSourceModel(self._packages_model)
        self.lstTools.setModel(self._filter_model)


    def connect_slots(self):
        self.edFilter.textChanged.connect(self.filter_chainged)

    def filter_chainged(self, text):
        self._filter_model.setFilterRegExp(QtCore.QRegExp(text))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = MainWindow(window)
    window.show()
    sys.exit(app.exec_())