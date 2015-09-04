#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Module containing the Dialog boxes for the GooDoc Application.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox)
from constants import *



class SettingsDialog(QDialog):
    """ Inherits: QDialog
        This class defines a dialog box.
        This dialog box is composed of two radio buttons, which let the user choose the order of methods and classes in the generated documentation.
    """

    def __init__(self, parent=None):
        """ Constructor
            Params: parent -> the object's parent
            Return: self
            The object is initialized with the super-constructror, the GUI with the initUI method.
        """
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        """ Object method
            Params: None
            Return: None
            This method sets the dialog box's layout.
            The Dialog box conatains two radio buttons and OK/Cancel buttons.
            sizeHint() sets the box to an ideal size.
        """

        #creating layout
        settings_layout = QVBoxLayout();

        #creating Radio buttons
        self.nat_order = QRadioButton("Natural order", self);
        self.alph_order = QRadioButton("Alphabetical", self);

        #creating the buttons
        buttons = QDialogButtonBox();

        #creating OK button and connecting it to the dialog
        buttons.addButton(QDialogButtonBox.Ok);
        buttons.accepted.connect(self.accept)
        
        #creating Cancel button and connecting it to the dialog
        buttons.addButton(QDialogButtonBox.Cancel);
        buttons.rejected.connect(self.reject)

        #adding created buttons to the layout
        settings_layout.addWidget(self.nat_order);
        settings_layout.addWidget(self.alph_order);
        settings_layout.addWidget(buttons);

        #adding layout to dialog
        self.setLayout(settings_layout);
        self.sizeHint()



    def exec_(self):
        """ Object method.
            Params: None.
            Return: None.
            This method displays the window and launches its event loop. 
            Changes are commited when the OK button is pressed.
        """ 
        # If changes was confirmed
        if(super().exec_()):
            
            if self.nat_order.isChecked():
                self.parent()._files._order = NATURAL_ORDER;
            elif self.alph_order.isChecked():
                self.parent()._files._order = ALPHABETICAL_ORDER;