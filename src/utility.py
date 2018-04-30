from PyQt5 import QtWidgets

class SubclassOfQStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter_, option_, index_):
        option_.showDecorationSelected = False
        super(SubclassOfQStyledItemDelegate,self).paint(painter_, option_, index_)
