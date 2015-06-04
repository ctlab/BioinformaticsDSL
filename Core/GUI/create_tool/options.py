from PyQt5 import QtCore

class Options(QtCore.QAbstractItemModel):
    def __init__(self):
        super(QtCore.QAbstractItemModel, self).__init__()
        self._options = []
        self.setHeaderData(0, QtCore.Qt.Horizontal, 'IO', QtCore.Qt.DisplayRole)
        self.setHeaderData(1, QtCore.Qt.Horizontal, 'name', QtCore.Qt.DisplayRole)
        self.setHeaderData(2, QtCore.Qt.Horizontal, 'repr', QtCore.Qt.DisplayRole)
        self.setHeaderData(3, QtCore.Qt.Horizontal, 'type', QtCore.Qt.DisplayRole)
        self.setHeaderData(4, QtCore.Qt.Horizontal, 'default', QtCore.Qt.DisplayRole)

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