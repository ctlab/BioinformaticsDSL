import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog
from PyQt5 import QtCore
from GUI.pipeline_editor.main_window_ui import Ui_MainWindow
from GUI.pipeline_editor.work_area import WorkArea
from GUI.pipeline_editor.connect_dialog import ConnectDialog
from GUI.create_tool.create_tool import CreateToolWidget
from GUI.create_io_steps.create_io_steps import CreateIOWidget
from package_manager import PackageManager
import xml.etree.ElementTree as ET
import os

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
        self.edFilter.textChanged.connect(self.filter_changed)
        self.btnAddStep.clicked.connect(self.add_step)
        self.btnConnect.clicked.connect(self.connect_steps)
        self.btnNewTool.clicked.connect(self.new_tool)
        self.btnSetIO.clicked.connect(self.set_io)
        self._work_area.params_chainged.connect(self.params_changed)

    def filter_changed(self, text):
        self._filter_model.setFilterRegExp(QtCore.QRegExp(text))

    def _get_pl_info(self, pl_path):
        args = []
        root = ET.parse(pl_path).getroot()
        for child in root:
            if child.tag in ('input', 'output'):
                arg = {'io' : child.tag[0], 'name': child.attrib['name'], 'type': child.attrib.get('type', 'void'), 'value': ''}
                args.append(arg)

        return args

    def add_step(self):
        idx = self.lstTools.selectionModel().currentIndex()
        data = self._filter_model.data(idx, QtCore.Qt.UserRole)
        pl_path = self._pm.find_pipeline(*data)
        args = self._get_pl_info(pl_path)

        step_name = "step_%s" % data[1]
        if step_name in self._work_area.get_steps_names():
            id = 2
            while True:
                original_name = step_name + ('_%d' % id)
                id += 1
                if original_name not in self._work_area.get_steps_names():
                    step_name = original_name
                    break
        self._work_area.add_step(step_name, args)

    def new_tool(self):
        d = QDialog()
        create_tool = CreateToolWidget(d)
        d.exec_()

    def set_io(self):
        d = QDialog()
        create_io = CreateIOWidget(d)
        result = d.exec_()
        if result == QDialog.Accepted:
            options = create_io.options.get_options()
            self._work_area.set_inputs([{'io': 'o', 'name': option[1], 'type': option[2], 'default': option[3]} for option in options if option[0] == 'input'])
            self._work_area.set_outputs([{'io': 'i', 'name': option[1], 'type': option[2], 'default': option[3]} for option in options if option[0] == 'output'])

    def connect_steps(self):
        d = QDialog()
        connect_dialog = ConnectDialog(d, self._work_area)
        result = d.exec_()
        if result == QDialog.Accepted:
            step_from = self._work_area.find_step(connect_dialog.cbOtherStep.currentText())
            output_ = connect_dialog.cbOtherStepOutput.currentText()
            step_to = self._work_area.get_selected_step()
            input_ = connect_dialog.cbMyInput.currentText()

            self._work_area.connect_steps(step_from, output_, step_to, input_)

    def params_changed(self):
        selected_step = self._work_area.get_selected_step()
        self.edSelectedName.setText(selected_step.get_name())
        self.tblSelectedStepArgs.setModel(selected_step.get_args_model())
        self.tblSelectedStepArgs.setColumnWidth(0, 20)
        self.tblSelectedStepArgs.setColumnWidth(1, 100)
        if selected_step._io:
            self.tblSelectedStepArgs.setColumnWidth(2, 50)
        self.tblSelectedStepArgs.horizontalHeader().setStretchLastSection(True)


    def create_pipeline(self, name):
        pl = ET.Element('pipeline')
        pl.set('name', name)

        for step in self._work_area._steps:
            step.add_to_pl(pl)

        return ET.tostring(pl, encoding='utf-8').decode("utf-8")

    def save(self):
        d = QFileDialog()
        file_name = d.getSaveFileName()
        pl_file = open(file_name, 'w')
        pl_file.write(self.create_pipeline(os.path.basename(file_name).split('.')[0]))
        pl_file.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = MainWindow(window)
    window.show()
    sys.exit(app.exec_())