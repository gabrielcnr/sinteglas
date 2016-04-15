from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pandas as pd
import numpy as np

class Column(object):
    def __init__(self, title, key, align='left', fmt='',
                 cell_style_callback=None):
        self.title = title
        self.key = key
        self.align = align
        self.fmt = fmt
        if cell_style_callback is None:
            cell_style_callback = self._default_cell_style_callback
        self.cell_style_callback = cell_style_callback

    def _default_cell_style_callback(self, array, index, role):
        return None



align_map = {
    'left': Qt.AlignVCenter | Qt.AlignLeft,
    'center': Qt.AlignVCenter | Qt.AlignCenter,
    'right': Qt.AlignVCenter | Qt.AlignRight,
}

DefaultColumn = Column(None, None, align='right', fmt='.1f')

GRID_FONT = QFont('Segoe UI')
GRID_FONT.setPixelSize(12)

HEADER_FONT = QFont('Segoe UI')
HEADER_FONT.setPixelSize(12)

HEADER_FONT_BOLD = QFont('Segoe UI')
HEADER_FONT_BOLD.setPixelSize(12)
HEADER_FONT_BOLD.setBold(True)



class Model(QAbstractTableModel):

    def __init__(self, df, columns=None, parent=None):
        super(Model, self).__init__(parent=parent)
        self.df = df
        self.row_count = len(df)
        self.col_count = len(df.columns)
        self.headers = list(df.columns)
        self.array = df.as_matrix()

        self.cols = {}
        for col in columns or []:
            if col.key in self.headers:
                self.cols[self.headers.index(col.key)] = col
            col.qt_align = align_map[col.align]

        DefaultColumn.qt_align = align_map[DefaultColumn.align]


    def rowCount(self, parent=None, *args, **kwargs):
        return self.row_count

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.col_count

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            col = self.cols.get(index.column(), DefaultColumn)
            return format(self.array[index.row(), index.column()], col.fmt)
        elif role == Qt.TextAlignmentRole:
            col = self.cols.get(index.column(), DefaultColumn)
            return col.qt_align
        elif role == Qt.FontRole:
            return GRID_FONT
        elif role == Qt.ForegroundRole:
            col = self.cols.get(index.column(), DefaultColumn)
            return col.cell_style_callback(self.array, index, role)


    def headerData(self, index, orientation, role=None):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                col = self.cols.get(index)
                if col is None:
                    return self.headers[index]
                else:
                    return col.title
            elif role == Qt.FontRole:
                return HEADER_FONT_BOLD

        else:
            if role == Qt.DisplayRole:
                return index+1 # TODO: return DataFrame index
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignVCenter | Qt.AlignRight
            elif role == Qt.FontRole:
                return HEADER_FONT


BLUE = QColor(Qt.blue)
DARKCYAN = QColor(Qt.darkCyan)
RED = QColor(Qt.red)

def custom_cell_style(array, index, role):
    if role == Qt.ForegroundRole:
        value = array[index.row(), index.column()]
        if value < 0.3:
            return BLUE
        elif 0.3 <= value < 0.8:
            return DARKCYAN
        else:
            return RED

columns = [
    Column('FOO', 'Column 2', align='center', fmt='.2f', cell_style_callback=custom_cell_style),
    Column('BAR', 'Column 4', align='right', fmt='.4f', cell_style_callback=custom_cell_style),
]

app = QApplication([])
df = pd.DataFrame(np.random.rand(100000, 200),
                  columns=['Column %d' % i for i in xrange(1, 201)])
model = Model(df, columns=columns)
view = QTableView()
view.setAlternatingRowColors(True)

view.verticalHeader().setResizeMode(QHeaderView.Fixed)
view.verticalHeader().setDefaultSectionSize(26)

view.setModel(model)
view.showMaximized()


app.exec_()


