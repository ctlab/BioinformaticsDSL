from GUI.pipeline_editor.connect_dialog_ui import Ui_Dialog

class ConnectDialog(Ui_Dialog):
    def __init__(self, parent, work_area):
        self.setupUi(parent)
        self._work_area = work_area
        self.cbMyInput.addItems(self._work_area.get_selected_step().get_inputs_names())
        self.cbOtherStep.addItems(self._work_area.get_steps_names())
        other = self.cbOtherStep.currentText()
        self.cbOtherStepOutput.addItems(self._work_area.find_step(other).get_outputs_names())
        self.cbOtherStep.currentIndexChanged[str].connect(self.other_step_chainged)

    def other_step_chainged(self, other):
        self.cbOtherStepOutput.clear()
        self.cbOtherStepOutput.addItems(self._work_area.find_step(other).get_outputs_names())