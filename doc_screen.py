#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" The doc_screen module represents the documentation screen.
"""
import sys
import os

from PyQt5.QtWidgets import (QWidget, QPushButton, QListView, QVBoxLayout, QHBoxLayout, QTabWidget, QAbstractItemView, QApplication)
from PyQt5.QtCore import QStringListModel

import html_gen
from list_view import ListView
from python_model import PythonModel
from constants import * 


class DocumentationScreen(QWidget):
    """ Inherits: QWidget
        Displays the documentation screen, used to generate HTML documentation.
        This screen has a button and Tab Bar, containing two QListView.
    """

    def __init__(self, parent=None):
        """ Constructor
            Params: parent -> the object's parent
            Return: self
            The object is initialized with the super-constructror, the GUI with the initUI method.
        """
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        """ Object method
            Params: None
            Return: None
            A QPushButton is created and added to the screen.
            A QTabWidget is created with initTabBar and added to the screen.
        """
        
        hbox = QHBoxLayout()

        # Button creation
        style_button = QPushButton(STYLE_BUTTON_TITLE)
        style_button.clicked.connect(self.parent().setStyleScreen)
        
        hbox.addWidget(style_button)

        # Tabbar Creation
        vbox = QVBoxLayout()
        self.initTabBar()
        vbox.addWidget(self.tab_bar)
        vbox.addLayout(hbox)
        
        # Layout definition
        self.setLayout(vbox)

        self.setWindowTitle("GooDoc")
        self.show()


    def initTabBar(self):
        """ Object method
            Params: None
            Return: None
            Initializes the QTabWidget of the documentation screen with an 'HTML' and a 'Python' tab.
            Each tab has a QListView. The model for the HTML QListView is a QStringListModel. For the Python QListView, the model is a PythonModel, defined in the python_model module.
        """

        # Model Creation
        html_model = QStringListModel()

        python_model = PythonModel()

        # Tab Bar Creation
        self.tab_bar = QTabWidget()

        # Each View has it own model
        html_view = ListView()
        html_view.setModel(html_model)
        html_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        html_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

        python_view = ListView()
        python_view.setModel(python_model)
        python_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        

        # Adds of the two tabs
        self.tab_bar.addTab(python_view, "Python")
        self.tab_bar.addTab(html_view , "HTML")


    def dragEnterEvent(self, event):
        """ Redefined Object method
            Params: QDragEnterEvent event -> Object dragged onto the widget
            Return: None
            If the event contains a file, it is droppable.
        """
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore() 

    def dropEvent(self, event):
        """ Redefined Object method
            Params: QDragEnterEvent event -> Object dragged onto the widget
            Return: None
            Finds the path of each file dropped onto the widget and sends it (if possible) to the addFiles method of the FileHandler object, attribute of the parent object.
        """
        files = []
        for url in event.mimeData().urls():
            files.append(url.toLocalFile())

        try:
            self.parent()._files.addFiles(files)
        except Exception:
            pass;
            



if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = DocumentationScreen()
    test.show()
    sys.exit(app.exec_())
        