#/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import re
import pickle
from html_gen import PythonFile
from constants import *


class StyleSheet:
    """ Inherits: None
        Class modeling a css style sheet.
    """

    def __init__(self, path, name = NEW_STYLE_NAME, user_style = True):
        """ Constructor
            Params: String name -> name of the style sheet, has NEW_STYLE_NAME (defined in constants module) for default value
                    String path -> The path of the corresponding CSS file
                    bool users_style -> Flag taking the True value when this is not a default style of the application. Has true for default value
            Initializes _path, _name and _user_style attributes.
        """
        self._path = path
        self._name = name
        self._user_style = user_style


class StyleHandler:
    """ Inherits: None
        Class modeling the style sheet handler, in the application.
        It has two attributes, _styles and parent.
    """

    def __init__(self, parent):
        """ Constructor
            Params: StyleScreen parent -> The screen which the style handler belongs to
            Return: None
            The _styles attribute is initialized with an empty list.
            The parent attribute is initialized with the 'parent' parameter.
            If a saved _styles list is found, load() is called.
            Else, initStyles() is called.
        """
        self._styles = []
        self.parent = parent
        if os.path.isfile(SAVE_FILE_PATH):
            self.load()
        else:
            self.initStyles()

    def __setitem__(self, index, value):
        """ Special method.
            Params: int index -> the index of the changed value in the list 
                    StyleSheet value -> the new value
            Return: None
            Reimplementing this method provides write access to _styles list, with syntax:
                self[index] = value
        """
        self._styles[index] = value

    def __getitem__(self, index):
        """ Special method
            Params: int index -> the index of the wanted object in the list
            Return: _styles[index]
            Reimplementing this method provides read access to _styles list, with syntax:
                self[index]
        """
        return self._styles[index]

    def __len__(self):
        """ Special method
            Params: None
            Return: length of _styles list
            Reimplementing this method allows access to _styles length with syntax:
                sh = StyleHandler(None)
                len(sh)
        """
        return len(self._styles)

    def pop(self, index=0):
        """ Object method
            Params: int index -> index of the object to remove, has 0 for default value
            Return: None
            Removes the object at _styles[index], and calls the save() method. The corresponding tab is also removed.
        """
        self._styles.pop(index)
        self.save()
        self.parent.tab_bar.removeTab(index)

    def append(self, style):
        """ Object method
            Params: StyleSheet style -> StyleSheet to append to _styles list
            Return: None
            Appends 'style' at the end of the list and calls save().
        """ 
        self._styles.append(style)
        self.save()


    def rename(self, index, new_name):
        """ Object method
            Params: int index -> index of the style to rename.
                    String new_name -> the new name of the style
            Return: None
            This method renames the style _styles[index] with the new_name string.
            Calls save().
        """
        self[index]._name = new_name
        self.save()

    def load(self):
        """ Object Method
            Params: None
            Return: None
            Loads the saved _styles used in a previous session.
            See also: save().
        """
        with open(SAVE_FILE_PATH, "rb") as f:
            depickler = pickle.Unpickler(f)
            self._styles = depickler.load()

    def save(self):
        """ Object Method
            Params: None
            Return: None
            Saves the _styles list in the saved_style file, at SAVE_FILE_PATH.
            See also: load().
        """
        with open(SAVE_FILE_PATH, "wb") as f:
            pickler = pickle.Pickler(f)
            pickler.dump(self._styles)


    def initStyles(self):
        """ Object method
            Params: None
            Return: None
            Sets up the default list of available style sheets.
        """
        self._styles.append(StyleSheet(STYLE_GOO_PATH, STYLE_GOO_NAME, False));
        self._styles.append(StyleSheet(STYLE_DEEPBLUE_PATH, STYLE_DEEPBLUE_NAME, False));
        self._styles.append(StyleSheet(STYLE_MELTDOWN_PATH, STYLE_MELTDOWN_NAME, False));
        self._styles.append(StyleSheet(STYLE_DOXYGEN_PATH, STYLE_DOXYGEN_NAME, False));

        if not os.path.isdir(SAVE_FOLDER_PATH):
            os.mkdir(SAVE_FOLDER_PATH)
        self.save()

    @staticmethod
    def setStyle(path, new_name):
        """ Static method
            Params: String path -> the file's path 
                    String new_name -> the style name
            Return: None
            Changes the style of the file, wich the path is given in params.
            The old style name is found and replaced by the new style name.
        """
        with open(path, "r+") as handler:
            text = handler.read()

        old_name = re.search(REGEX_STYLE, text).group("style")
        text = text.replace(old_name, new_name)

        with open(path, "w") as handler:
            handler.write(text)
