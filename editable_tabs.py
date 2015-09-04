#!/usr/bin/python3
# -*- encoding:utf-8 -*-

""" editable_tabs module.
    Implements the classes used to create editable tab labels in the style screen.
    This module is primarily based off of code published here : http://stackoverflow.com/questions/8707457/pyqt-editable-tab-labels
    All credit goes to stackoverflow user ekhumoro.
    Main changes : update to use of PyQt5, class names.
"""
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QTabBar, QTabWidget, QApplication, QLineEdit, QWidget

class EditableTabBar(QTabBar):
    """ Inherits: QTabBar
        Implements editable label behaviour to tabs.
    """
    def __init__(self, parent=None):
        """ Constructor
            Params: QWidget parent -> object's parent
            Defines attributes:
                window as arg parent
                _editor as a QLineEdit object
        """
        super().__init__(parent)
        self.window = parent
        self._editor = QLineEdit(self)
        self._editor.setWindowFlags(Qt.Popup) #helps set location
        self._editor.setFocusProxy(self) #determines focus handling
        self._editor.editingFinished.connect(self.handleEditingFinished)
        self._editor.installEventFilter(self) #allows use of overloaded function eventFilter() to handle events

    def eventFilter(self, widget, event):
        """ Overloaded object method
            Params: QObject widget -> watched object (here: self)
                    QEvent event -> the event that is handled
            Return: True if the event is handled
                    Return value of QTabBar.eventFilter() if the event is not handled (bool)
            Determines editing is canceled if a click event is recorded outside of the _editor or if [esc] is pressed by hiding the _editor object.
            Else, the event is passed on to the parent class.
        """
        if ((event.type() == QEvent.MouseButtonPress and not self._editor.geometry().contains(event.globalPos())) or (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape)):
            self._editor.hide()
            return True
        return QTabBar.eventFilter(self, widget, event)

    def mouseDoubleClickEvent(self, event):
        """ Overloaded object method
            Params: QEvent event -> the event that is handled
            Return: None
            Calls editTab() for the tab at which the double click event is recorded
        """
        index = self.tabAt(event.pos())
        if index >= 0 and self.window._styles[index]._user_style:
            self.editTab(index)

    def editTab(self, index):
        """ Object method
            Params: int index -> index of the tab to edit
            Return: None
            Sets the _editor's text, size and position to the tab label's and shows it.
        """
        rect = self.tabRect(index)
        self._editor.setFixedSize(rect.size())
        self._editor.move(self.window.mapToGlobal(rect.topLeft()))
        self._editor.setText(self.tabText(index))
        if not self._editor.isVisible():
            self._editor.show()

    def handleEditingFinished(self):
        """ Object method
            Params: None
            Return: None
            Hides the _editor and sets the entered string as the new tab label.
            Called at the automatic call of self._editor.editingFinished()
        """
        index = self.currentIndex()
        if index >= 0:
            self._editor.hide()
            new_name = self._editor.text()
            self.window._styles.rename(index, new_name)
            self.setTabText(index, new_name)

class EditableTabWidget(QTabWidget):
    """ Inherits: QTabWidget
        When used in place of QTabWidget, allows its tabBar to have editable tabs without manually replacing the object's tabBar with setTabBar().
    """
    def __init__(self, parent=None):
        """ Constructor
            Sets the tabBar to an EditableTabBar.
        """
        super().__init__(parent);
        tabBar=EditableTabBar(parent);
        self.setTabBar(tabBar);


if __name__ == '__main__':
    #test code for the module
    import sys
    app = QApplication(sys.argv)
    window = EditableTabWidget()
    window.addTab(QWidget(window), 'Tab One')
    window.addTab(QWidget(window), 'Tab Two')
    window.show()
    sys.exit(app.exec_())