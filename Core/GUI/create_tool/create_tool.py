import sys
from os import path
import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

from GUI.create_tool.create_tool_widget_ui import Ui_CreateTool
from GUI.create_tool.options import Options


class CreateToolWidget(Ui_CreateTool):

    def __init__(self, parent):
        self._parent = parent
        self.setupUi(parent)
        self.options = Options()
        self.tblOptions.setModel(self.options)
        self.cbIO.addItems(['input', 'output'])
        self.connect_slots()

    def connect_slots(self):
        self.btnExit.clicked.connect(self.on_exit)
        self.btnSave.clicked.connect(self.on_save)
        self.btnAddOpt.clicked.connect(self.on_add_option)

    def on_exit(self):
        self._parent.close()

    def on_save(self):
        d = QFileDialog()
        save_dir = d.getExistingDirectory()
        pl_file = open(path.join(save_dir, self.edToolName.text() + '.xml'), 'w')
        pl_file.write(self.create_pipeline())
        pl_file.close()
        self._parent.close()

    def on_add_option(self):
        self.options.add_option(self.cbIO.currentText(), self.edOptName.text(), self.edOptType.text(),  self.edOptRepr.text(), self.edOptDef.text())
        self.edFormat.setText(self.edFormat.text() + (' $(%s)' % self.edOptName.text()))

    def create_pipeline(self):
        pl = ET.Element('pipeline')
        pl.set('name', self.edToolName.text())

        for option in self.options.get_options():
            opt = ET.SubElement(pl, option[0])
            opt.set('name', option[1])
            opt.set('type', option[2])
            if option[3]:
                opt.set('repr', option[3])
            if option[4]:
                opt.set('default', option[4])

        fmt = ET.SubElement(pl, 'sh')
        fmt.set('c', self.edFormat.text())

        return ET.tostring(pl, encoding='utf-8').decode("utf-8")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    ui = CreateToolWidget(window)
    window.show()
    sys.exit(app.exec_())