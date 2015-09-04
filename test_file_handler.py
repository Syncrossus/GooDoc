#/usr/bin/python3
# -*- coding:utf-8 -*-

""" This module provides all unitary tests of the file_handler module. """

import os
import sys
import shutil

from PyQt5.QtWidgets import QApplication

import unittest
from html_gen import PythonFile
from file_handler import FileHandler
from goodoc import Window
from constants import *



class TestFileHandler(unittest.TestCase):
    """ Inherits: unittest.TestCase
        This class provides all unitary test of the FileHandler class. 
    """

    def setUp(self):
        """ Object method
            Params: None
            Return: None
            This method is called before each unitary test.
            It set up environnement before the test.
            An attributes file_handler, FileHandler's object is added to the class.
        """
        self.goodoc = Window()


    def test_extractFiles(self, folder = os.path.dirname(__file__)):
        """ Object method
            Params: folder (str) -> tested folder's path, has the directory path of the current file for default value.
            Return: None
            This method tests the behaviour of the extractFiles method.
            This method is called with folder as param.
            Each returned file needs to be a python or an html file.
            Then, the content of the dir 'folder', given as params, is returned.
            Each files of the dir needs to be in the return of extractFiles.
            For each subfolder in the dir, this current method is called.
        """
        
        files = [os.path.basename(f) for f in FileHandler.extractFiles(folder)]

        for f in files: 
            extension = os.path.splitext(f)[1]
            self.assertTrue(extension in (".pyw", ".py", ".html", ".htm"))
        
        dir_content = os.listdir(folder)  
        for el in dir_content:

            if os.path.isfile(el) and os.path.splitext(el)[1] in (".pyw", ".py", ".html", ".htm"):
                    self.assertTrue(el in files)

            if os.path.isdir(el):
                path = folder + "/" + el
                self.test_extractFiles(path) 


    def test_addFiles(self, test_list=["test.py","test.html","test.jpg"]):
        """ Object method
            Params: test_list (list) -> tested list, has list with python, html and jpeg path for default value. 
            Return: None
            This method tests the behaviour of the addFiles method.
            A list is given to the addFiles method.
            Each file path in the _pythonFiles needs to be a python file path.
            Each file path in the _htmlFiles needs to be a html file path.
        """

        self.goodoc._files.addFiles(test_list)

        for el in self.goodoc._files._pythonFiles:
            self.assertEqual(type(el), PythonFile)

        for el in self.goodoc._files._htmlFiles:
            extension = os.path.splitext(el)[1]
            self.assertTrue(extension in (".htm",".html"))

    def test_processFiles(self):
        """ Object method
            Params: None
            Return: None
            This method tests the behaviour of the processFiles method.
            processFiles is called on the content of the current dir.
            A documentation's folder needs to be created and every files in this folder needs to correspond to a python file in the tested folder.
        """
        # Creation of the python and html list
        folder = os.path.dirname(__file__)
        files = self.goodoc._files.extractFiles(folder)
        self.goodoc._files.addFiles(files)

        # backup of the python file, rename on html file
        python_files = [os.path.splitext(os.path.basename(f._name))[0] + ".html" for f in self.goodoc._files._pythonFiles]

        self.goodoc._files.processFiles()

        # Verification of the generated information
        self.assertTrue(os.path.isdir(self.goodoc._files._path))
        directory_content = os.listdir(self.goodoc._files._path)

        for el in python_files:
            self.assertTrue(el in directory_content)

        shutil.rmtree(self.goodoc._files._path)


if __name__=="__main__":
    app = QApplication(sys.argv)
    unittest.main()
    #app.exec_()
    

