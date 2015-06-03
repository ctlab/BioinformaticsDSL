import sys
from os import path
import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

from GUI.create_tool.main_window_ui import Ui_Form
from GUI.create_tool.options import Options


class MainWindow(Ui_Form):

    def __init__(self, form):
        self.setupUi(form)
        self.options = Options()
        self.tblOptions.setModel(self.options)
        self.cbIO.addItems(['input', 'output'])
        self.connect_slots()

    def connect_slots(self):
        self.btnExit.clicked.connect(self.on_exit)
        self.btnSave.clicked.connect(self.on_save)
        self.btnAddOpt.clicked.connect(self.on_add_option)

    def on_exit(self):
        exit(0);

    def on_save(self):
        d = QFileDialog()
        save_dir = d.getExistingDirectory()
        pl_file = open(path.join(save_dir, self.edToolName.text() + '.xml'), 'w')
        pl_file.write(self.create_pipeline())
        pl_file.close()
        exit(0);

    def on_add_option(self):
        self.options.add_option(self.cbIO.currentText(), self.edOptName.text(), self.edOptRepr.text(),  self.edOptType.text(), self.edOptDef.text())

    def create_pipeline(self):
        pl = ET.Element('pipeline')
        pl.set('name', self.edToolName.text())

        for option in self.options.get_options():
            opt = ET.SubElement(pl, option[0])
            opt.set('name', option[1])
            opt.set('repr', option[2])
            opt.set('type', option[3])
            opt.set('default', option[4])

        fmt = ET.SubElement(pl, 'sh')
        fmt.set('c', self.edFormat.text())

        return ET.tostring(pl, encoding='utf-8').decode("utf-8")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    ui = MainWindow(window)
    window.show()
    sys.exit(app.exec_())