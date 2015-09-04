#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Main Module of the GooDoc Application.
    The application is started by launching this module.
    It contains the Window class and the main procedure.
"""

import sys
import os

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAbstractItemView, QListView, QAction, QDialog, QFileDialog, QDialogButtonBox, QRadioButton, QToolBar, QVBoxLayout)
from PyQt5.QtGui import QIcon

from doc_screen import DocumentationScreen
from style_screen import StyleScreen
from dialogs import SettingsDialog
from file_handler import FileHandler
from html_gen import PythonFile
from constants import *



class Window (QMainWindow):
    """ Inherits: QMainWindow
        This class is the main class of the application.
        It contains a FileHandler (file_handler module) containing the python and HTML files managed in the application.
        It sets consecutively as central widget a DocumentationScreen (doc_screen module) and a StyleScreen (style_screen module).
    """

    def __init__(self):
        """ Constructor
            Params: None
            Return: self
            This method creates the file handler. Then the documentation screen is set as central widget.
        """
        super().__init__();
        self._files = FileHandler(self);
        self.setDocumentationScreen();

    def setStyleSheet(self, path):
        with open(path, "r") as handler:
            style_sheet = handler.read()

        super().setStyleSheet(style_sheet)


    ## Documentation ##

    def setDocumentationScreen(self):
        """ Object method
            Params: None
            Return: None
            This method sets up the documentation screen.
            A DocumentationScreen widget is created and set as the central widget.
            This method calls createToolBar.
        """
        docScreen = DocumentationScreen(self);

        self.setCentralWidget(docScreen)
        self.createToolBar()

        self.setStyleSheet(DOCSCREEN_STYLESHEET_PATH)
        self.setWindowTitle(DOCUMENTATION_TITLE);
        self.setGeometry(100,100, 1200, 600);
        self.show();


    def createToolBar(self):
        """ Object method
            Params: None
            Return: None
            Creates a ToolBar with 4 buttons connected to 4 methods : fileSelectDialog(), dirSelectDialog(), FileHandler.processFiles() and settings().
        """
        self.toolbar = QToolBar(self);
        
        addFileAction = QAction(QIcon(ADD_FILES_ICON), ADD_FILES_TIP, self);
        addFileAction.setShortcut(ADD_FILES_SHORTCUT);
        addFileAction.triggered.connect(self.fileSelectDialog);

        addDirAction = QAction(QIcon(ADD_DIR_ICON), ADD_DIR_TIP, self);
        addDirAction.setShortcut(ADD_DIR_SHORTCUT);
        addDirAction.triggered.connect(self.dirSelectDialog);

        startGenAction=QAction(QIcon(START_ICON), START_TIP, self);
        startGenAction.setShortcut(START_SHORTCUT);
        startGenAction.triggered.connect(self._files.processFiles);

        settingsAction=QAction(QIcon(SETTINGS_ICON), SETTINGS_TIP, self);
        settingsAction.setShortcut(SETTINGS_SHORTCUT);
        settingsAction.triggered.connect(self.settings);


        self.addToolBar(self.toolbar);
        self.toolbar.addAction(addFileAction);
        self.toolbar.addAction(addDirAction);
        self.toolbar.addAction(startGenAction);
        self.toolbar.addAction(settingsAction);


    def settings(self):
        """ Object method
            Params: none
            Return: none
            Opens a settings dialog.
        """
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()


    def fileSelectDialog(self):
        """ Object method
            Params: none
            Return: none
            Opens a file selection dialog and adds all selected python and html files to the list of files to process.
        """
        
        file_dialog = QFileDialog();
        file_dialog.setFileMode(QFileDialog.ExistingFiles);

        if file_dialog.exec_() :
	        self._files.addFiles(file_dialog.selectedFiles());

    def dirSelectDialog(self):
        """ Object method
            Params: none
            Return: none
            Opens a folder selection dialog and adds all python and html files in selected folder to the list of files to process.
        """
        file_dialog = QFileDialog();
        file_dialog.setFileMode(QFileDialog.Directory);
        
        if file_dialog.exec_():
	        directories = file_dialog.selectedFiles()
	        if len(directories) > 0:
	            self._files.addFiles(directories);

    ## Stylesheets ##

    def setStyleScreen(self):
        """ Object method
            Params: none
            Return: none
            Creates the Style screen and sets it as central widget. The toolbar is removed and the window title is changed.
        """
        
        if self._files.processFiles():
            style_screen = StyleScreen(self)
            self.setCentralWidget(style_screen)
            self.setStyleSheet(STYLESCREEN_STYLESHEET_PATH)
            self.removeToolBar(self.toolbar)
            self.setWindowTitle(STYLE_TITLE);


if __name__ == "__main__":
    app = QApplication(sys.argv);
    goodoc = Window();
    sys.exit(app.exec_());
