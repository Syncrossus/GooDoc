#/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import shutil
from style_handler import StyleHandler
from html_gen import PythonFile
from constants import *


class FileHandler:
    """ Manages all the python and html files of the application. 
        It can add files in the correct list, by reading their extension, call the documentation generation of the python files and add a style to the html files.
        Contains a list of python files and a list of html files.
    """

    def __init__(self, parent=None):
        """ Constructor. 
            Params: Window (goodoc module) parent -> the parent of the file handler.
            return: self
        """
        self._pythonFiles = [];
        self._htmlFiles = [];
        self._order = NATURAL_ORDER;
        self._path = ""
        self._parent = parent;


    def addFiles(self, content_given):
        """ Object method
            Params: List content_given -> a list of files and directories
            Return: None
            Adds files to the correct list.
            For each content_given's element, if it is a python or html file, it is appended to the correct list.
            If it is a directory, extractFiles() is called.
            For each element of the files list, it reads the extension and adds it to the correct list.
        """
        files = []

        # files list creation
        for el in content_given:

            # File case
            if os.path.isfile(el):
                files.append(el)

            # Dir case
            if os.path.isdir(el):
                files += self.extractFiles(el)

        # Each element is put in the correct list, and views are updated.
        for name in files:

            if self._path == "":
                self._path =  os.path.join(os.path.dirname(name), NAME_CREATED_FOLDER);

            extension = os.path.splitext(name)[1]

            # Python files
            if extension in ('.py','.pyw'):
                self._pythonFiles.append(PythonFile(name));
                self._pythonFiles=list(set(self._pythonFiles)); #removing duplicates
                python_list = self._parent.centralWidget().tab_bar.widget(0)
                python_list.model().setPythonList(self._pythonFiles)

            # Html files
            elif extension in ('.html','.htm'):
                self._htmlFiles.append(name);
                self._htmlFiles=list(set(self._htmlFiles)); #removing duplicates
                html_list = self._parent.centralWidget().tab_bar.widget(1)
                html_list.model().setStringList(self._htmlFiles)
                

    @staticmethod
    def extractFiles(folder):
        """ Static method.
            Params : String folder
            Return Value : List containing path names of all files in specified folder and its subfolders
        """

        #two lists are needed to avoid skipping files when doing operations on the source list
        content = os.listdir(folder);
        files = []

        #fix for listdir not returning full path names
        for i in range(0, len(content)):
            content[i] = folder + "/" + content[i];


        for el in content:

            #keep only files with desired extensions
            if os.path.isfile(el):
                extension = os.path.splitext(el)[1]
                if extension in AUTHORIZED_EXTENSIONS:
                    files.append(el);

            #if el is a directory, recurse into it
            elif os.path.isdir(el):
                files += FileHandler.extractFiles(el);

        return files;


    def processFiles(self):
        """ Object method.
            Param: None.
            Return: boolean
            Method generating the documentation of all python files of the application.
            The folder wich is containing the generated documentation is first created, if it's necessary.
            If the folder's path is "", there is nothing to do, the method return false.
            Then, javascript file are copied into the folder.
            For each python file, the method save is called.
            Then, the path of generated html file is added to the htmlFiles list.
            The method then return True.
        """
        if self._path == "":
            return False

        if not os.path.exists(self._path) and self._pythonFiles != []:
            os.mkdir(self._path)
        shutil.copy(JAVASCRIPT_FILE_PATH, self._path)

        for f in self._pythonFiles:
            self._htmlFiles.append(f.save(self._path, self._order))
            
        self._pythonFiles = []

        html_list = self._parent.centralWidget().tab_bar.widget(1)
        html_list.model().setStringList(self._htmlFiles)
        python_list = self._parent.centralWidget().tab_bar.widget(0)
        python_list.model().setPythonList(self._pythonFiles)
        return True

    def processStyles(self, style_path):
        """ Object method
            Params: style_path (str) -> The style's path
            Return: None
            Applies the style of style_path to the documentation and copies it into the created dir.
        """
        style_name = os.path.basename(style_path)

        for html_file in self._htmlFiles:
            StyleHandler.setStyle(html_file, "'"+style_name+"'")

        shutil.copyfile(style_path, self._path + "/" + style_name)








    
