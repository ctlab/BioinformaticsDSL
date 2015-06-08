from GUI.create_io_steps.create_io_steps_widget_ui import Ui_CreateIO
from GUI.create_io_steps.options import Options


class CreateIOWidget(Ui_CreateIO):

    def __init__(self, parent):
        self._parent = parent
        self.setupUi(parent)
        self.options = Options()
        self.tblOptions.setModel(self.options)
        self.cbIO.addItems(['input', 'output'])
        self.connect_slots()

    def connect_slots(self):
        self.buttonBox.accepted.connect(self._parent.accept)
        self.buttonBox.rejected.connect(self._parent.reject)
        self.btnAddOpt.clicked.connect(self.on_add_option)

    def on_add_option(self):
        self.options.add_option(self.cbIO.currentText(), self.edOptName.text(), self.edOptType.text(),  self.edOptDef.text())