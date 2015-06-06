import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import QtCore
from GUI.pipeline_editor.main_window_ui import Ui_MainWindow
from GUI.pipeline_editor.work_area import WorkArea
from GUI.pipeline_editor.connect_dialog import ConnectDialog
from GUI.create_tool.create_tool import CreateToolWidget
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
        self.btnNewTool.clicked.connect(self.new_tool)
        self._work_area.params_chainged.connect(self.params_chainged)

    def filter_chainged(self, text):
        self._filter_model.setFilterRegExp(QtCore.QRegExp(text))

    def _get_pl_info(self, pl_path):
        args = []
        root = ET.parse(pl_path).getroot()
        for child in root:
            if child.tag in ('input', 'output'):
                arg = {'io' : child.tag[0], 'name' : child.attrib['name'], 'type' : child.attrib.get('type', 'void'), 'value' : ''}
                args.append(arg)

        return args

    def add_step(self):
        idx = self.lstTools.selectionModel().currentIndex()
        data = self._filter_model.data(idx, QtCore.Qt.UserRole)
        pl_path = self._pm.find_pipeline(*data)
        args = self._get_pl_info(pl_path)

        step_name = "step_%s" % data[1]
        if (step_name in self._work_area.get_steps_names()):
            id = 2
            while True:
                original_name = step_name + ('_%d' % id)
                id += 1
                if (original_name not in self._work_area.get_steps_names()):
                    step_name = original_name
                    break
        self._work_area.add_step(step_name, args)

    def new_tool(self):
        d = QDialog()
        create_tool = CreateToolWidget(d)
        d.exec_()


    def connect_steps(self):
        d = QDialog()
        connect_dialog = ConnectDialog(d, self._work_area)
        result = d.exec_()
        if result == QDialog.Accepted:
            step_from = self._work_area.find_step(connect_dialog.cbOtherStep.currentText())
            output = connect_dialog.cbOtherStepOutput.currentText()
            step_to = self._work_area.get_selected_step()
            input = connect_dialog.cbMyInput.currentText()

            self._work_area.connect_steps(step_from, output, step_to, input)

    def params_chainged(self):
        selected_step = self._work_area.get_selected_step()
        self.edSelectedName.setText(selected_step.get_name())
        self.tblSelectedStepArgs.setModel(selected_step.get_args_model())
        self.tblSelectedStepArgs.setColumnWidth(0, 20)
        self.tblSelectedStepArgs.setColumnWidth(1, 100)
        self.tblSelectedStepArgs.setColumnWidth(2, 50)
        self.tblSelectedStepArgs.horizontalHeader().setStretchLastSection(True)

    def save(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = MainWindow(window)
    window.show()
    sys.exit(app.exec_())