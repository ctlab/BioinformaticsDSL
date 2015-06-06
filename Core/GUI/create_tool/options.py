from PyQt5 import QtCore

class Options(QtCore.QAbstractItemModel):
    def __init__(self):
        super(QtCore.QAbstractItemModel, self).__init__()
        self._options = []

    def add_option(self, io_type, name, repr, type, default):
        new_row_id = len(self._options)
        self.beginInsertRows(QtCore.QModelIndex(), new_row_id, new_row_id)
        self._options.append((io_type, name, repr, type, default))
        self.endInsertRows()

    def get_options(self):
        return self._options


    def rowCount(self, in_index):
        return len(self._options)

    def columnCount(self, in_index):
        return 5

    def index(self, in_row, in_column, in_parent=None):
        return QtCore.QAbstractItemModel.createIndex(self, in_row, in_column)

    def data(self, in_index, role):
        if not in_index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            return self._options[in_index.row()][in_index.column()]

    def headerData(self, id, orient, role=None):
        if orient != QtCore.Qt.Horizontal or role != QtCore.Qt.DisplayRole:
            return None

        return ['io', 'name', 'type', 'repr', 'default'][id]


