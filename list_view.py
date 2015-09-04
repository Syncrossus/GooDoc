
#!/usr/bin/python3
# -*- encoding:utf-8 -*-

""" list_view module.
    Implements the list view object used in Goodoc.
    It contains the ListView class.
"""
from PyQt5.QtWidgets import QListView
from PyQt5.QtCore import Qt

class ListView(QListView):
    """ Inherits: QListView
        It has the same behaviour as QListView, but implements element deletion by pressing [DEL].
    """

    def __init__(self, parent=None):
        """ Constructor
            Params: DocumentationScreen parent -> the object's parent
            It only calls the super constructor.
        """
        super().__init__(parent)

    def keyPressEvent(self, event):
        """ Object method
            Params: QKeyEvent event -> the pressed key
            Return: None
            Method called when a key is pressed.
            If the pressed key is the delete key, all selected rows are deleted by calling removeSelectedIndexes().
        """
        if event.key() == Qt.Key_Delete:
            self.removeSelectedIndexes()

    def removeSelectedIndexes(self):
        """ Object method
            Params: None
            Return: None
            Called by keyPressEvent().
            Removes all selected rows (calls removeRow()).
        """
        indexes = sorted([index.row() for index in self.selectedIndexes()], reverse=True)
        for index in indexes:
            self.model().removeRow(index)



