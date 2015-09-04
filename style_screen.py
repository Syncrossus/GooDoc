#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" The style_screen module modeling the stylesheet selection screen.
    It contains the class StyleScreen.
"""
import sys
import os
import random

from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QTabWidget, QTabBar, QInputDialog)
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon

from constants import * 
from style_handler import StyleHandler, StyleSheet
from editable_tabs import EditableTabWidget

class StyleScreen(QWidget):
    """ Inherits: QWidget
        Class modeling the stylesheet selection screen. 
        This class displays the style screen, used to add stylesheets to HTML documentation.
        This screen has a Tab Bar, containing QWebviews.
        The confirm button is located below this tab bar.
    """

    def __init__(self, parent=None):
        """ Constructor
            Params: Window parent -> The screen's parent.
            Calls the super constructor and initUI().
        """
        super().__init__(parent)
        self._styles = StyleHandler(self);
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        """ Object method
            Params: None
            Return: None
            This method initializes the layout of the StyleScreen.
            The tab bar is created, a new tab is created for each stylesheet registered by the application.
            The tab bar has closable and renamable tabs (see editable_tabs module).
            A push button is created below the tab bar.
        """ 
        vbox = QVBoxLayout()

        self.tab_bar = EditableTabWidget(self)
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.tabCloseRequested[int].connect(self._styles.pop)
        self.tab_bar.currentChanged[int].connect(self.changeStyle)

        template = list()
        path = random.choice(self.parent()._files._htmlFiles)
        self._chosen_file = QUrl.fromUserInput(path)

        for i in range(len(self._styles)):
            # QWebview creation
            template.append(WebView(self))
            template[i].load(self._chosen_file)
            
            # Tab creation
            self.tab_bar.addTab(template[i], self._styles[i]._name);
            if self._styles[i]._user_style == False:
                self.tab_bar.tabBar().tabButton(i, QTabBar.RightSide).resize(0,0)

        button = QPushButton(CONFIRM_BUTTON_NAME, self)
        button.clicked.connect(self.confirm)

        vbox.addWidget(self.tab_bar)
        vbox.addWidget(button)
        self.setLayout(vbox)


    def addStyle(self, path):
        """ Object method
            Params: String path -> the local absolute path of the CSS file.
            Return: None
            This method is called to register an assignable StyleSheet in the application. 
            A new tab is created and a new stylesheet is appended to the _styles list.
            Called when a CSS file is dragged and dropped onto the StyleScreen.
        """
        # WebView Creation
        new_template = WebView(self)
        new_template.load(self._chosen_file)

        # Style creation and adds to the _styles list.
        new_style = StyleSheet(path, NEW_STYLE_NAME)
        self._styles.append(new_style)  

        # Tab creation
        self.tab_bar.addTab(new_template, new_style._name)


    def changeStyle(self, index):
        """ Object method
            Params: int index -> the index of the active tab
            Return: None
            Changes the style applied to the HTML files, using the index of the active tab.
            This method is called each time the active tab is changed.
            This applies a soft StyleSheet change (the HTML files are not modified).
        """
        new_name = "'" + QUrl.fromUserInput(os.path.realpath(self._styles[index]._path)).url() + "'"
        StyleHandler.setStyle(self._chosen_file.toLocalFile(), new_name)
        self.tab_bar.widget(index).load(self._chosen_file)
        old_name = new_name

    def confirm(self):
        """ Object method
            Params: None
            Return: None
            Confirms the chosen style and adds it to the generated documentation.
            The chosen style is the style of the current tab.
            This applies a hard StyleSheet change (the HTML files are modified).
        """
        index = self.tab_bar.currentIndex()
        style_path = self._styles[index]._path
        self.parent()._files.processStyles(style_path)
        self.parent().close()


class WebView(QWebView):
    """ Inherits: QWebView
        Class reimplementing the drag&drop.
        Only CSS files can be dragged into the WebView.
        If a CSS files is dropped, then StyleScreen.addStyle() is called.
    """
    def __init__(self, screen):
        """ Constructor
            Params: StyleScreen screen -> The screen which the WebView belongs to
            Return: None
            The super constructor is called, then dragging & dropping is enabled.
            The WebView.screen attribute is initialized with the screen parameter.
        """
        super().__init__()
        self.setAcceptDrops(True)
        self.screen = screen

    def dragEnterEvent(self, event):
        """ Object method
            Params: QDragEnterEvent event -> the dragged object
            Return: none
            This method defines the acceptation criteria of dragged objects.
            If event is a CSS file, it is accepted.
        """
        extension = os.path.splitext(event.mimeData().urls()[0].toLocalFile())[1]
        if event.mimeData().hasUrls() and extension == ".css":
            event.accept()
        else:
            event.ignore() 

    def dropEvent(self, event):
        """ Object Method
            Params: QDropEvent event -> the drop object
            Return: None
            This method is called when a drop event occurs.
            The CSS file's path is sent to StyleScreen.addStyle().
        """
        print(type(event))
        url = QUrl(event.mimeData().urls()[0])
        self.screen.addStyle(url.toLocalFile())
