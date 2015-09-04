#!/usr/bin/python3
# -*- coding:utf-8 -*-

""" This module represents a Python Model. 
    It contains class PythonModel.
"""

from PyQt5.QtCore import (QAbstractListModel, Qt, QVariant, QModelIndex)
from constants import *

class PythonModel(QAbstractListModel):
    """ Inherits: QAbstractListModel
        Class representing a model for a list of PythonFile objects.
        This model is used by ListView in the documentation screen.
    """

    def __init__(self, python_list=[]):
        """ Constructor
            Params: List python_list -> the data represented by the model
            Return: None
            The super constructor is called.
            Initializes attribute _python_files to python_list.
        """
        super().__init__()
        self._python_files = python_list


    def rowCount(self, parent=QModelIndex()):
        """ Object method
            Params: QModelIndex parent -> for tree organization, a parent is requested. Has invalid QModelIndex for default value
            Return: Number of rows displayed by the model (length of the _python_files list)
        """
        return len(self._python_files)

    def data(self, index, role = Qt.DisplayRole):
        """ Object method
            Params: QModelIndex index -> the data's index which needs to be accessed
                    ItemDataRole role -> the role of the accessed data
            Return: Data at the given index
            If this index is valid, lower than the length of the python_files list and the given role is Qt.DisplayRole, the correct data is returned.
            Else a QVariant() object is returned.
        """
        if not index.isValid() or index.row() >= len(self._python_files) or role != Qt.DisplayRole:
            return QVariant()

        else:
            return self._python_files[index.row()]._name + ".py"

    def removeRow(self, index, parent = QModelIndex()):
        """ Object method
            Params: int index -> index to remove
                    parent -> the row's parent, has an invalid QModelIndex for default value
            Return: None
            Removes the element, referenced by index.
            This method calls QAbstractListModel.beginRemoveRows() before deletion and QAbstractListModel.endRemoveRows() after it.
        """
        self.beginRemoveRows(parent, index, index+1)
        self._python_files.pop(index)
        self.endRemoveRows()


    def setPythonList(self, python_list):
        """ Object method
            Params: List python_list -> the new python list
            Return: None
            This method sets the _python_files list to the list given in params. 
            It calls QAbstractListModel.beginResetModel() before the change, and QAbstractListModel.endResetModel() after. 
            These methods are used to display the list change on the view.
        """
        self.beginResetModel()
        self._python_files = python_list
        self.endResetModel()


