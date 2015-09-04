#!/usr/bin/python3
#-*- coding:utf-8 -*-

""" Module providing unitary tests needed for the html_gen validation. """

import os
import unittest
import re
import html_gen
from constants import *



class TestPythonElement(unittest.TestCase):
    """ Inherit: unittest.TestCase
        This class provides a unitary test for each testable method of PythonElement class.
    """


    def setUp(self, name="test"):
        """ Object method.
            Param: name (str) -> the name of the python element, given to the constructor.
            Return: none
            Method called before each test, wich initialize it.
            It create a PythonElement as attribute, named python_el.
        """
        self.python_el = html_gen.PythonElement(name)


    def test_initDocstring(self, docstring="Hello\nWorld\n", indentation_level=2):
        """ Object method
            Params: docstring (str) -> a template docstring, used for test the method behaviour.
                   indentation_level (int) -> a random indentation level, given to the method.
            Return: None
            This method tests the initDocstring behaviour. 
            The number of '\\n' and it remplacement string are stored. The initDocstring method is then called. 
            The number of remplacement occurence needs to be equal to the sum of the two count, calculated before the initDocstring call.
        """
        count_new_line = docstring.count('\n')
        remplacement = "<br />\n" + "\t"*indentation_level
        count_remplacement = docstring.count(remplacement)
        self.python_el.initDocstring(docstring, indentation_level)
        self.assertTrue(self.python_el._docstring.count(remplacement), count_new_line + count_remplacement)






class TestPythonFile(unittest.TestCase):
    """ Inherit: unittest.TestCase
        This class provides each unitary test needed for the PythonFile class validation.
    """


    def setUp(self, path=__file__):
        """ Object method
            Params: path (str) -> path to the tested file, has the current file's path for default value.
            Return: None
            Method called before each test, initializing it. 
            An attribute python_file, object of the PythonFileClass is added.
        """
        self.python_file = html_gen.PythonFile(path)



    def test_extractClasses(self, number_class=3):
        """ Object method.
            Params: number_class (int) -> the number of class contained in the tested file. Has 3 for default value.
            Return: None
            This method tests the behaviour of the extractClasses method.
            The list _classes is initialize with an empty list.
            extractClasses is called on the content of the tested file.
            The length of the _classes list needs to be equal to the number_class param.
        """

        self.python_file._classes = []
        with open(__file__, "r") as file_resource:
            data = file_resource.read()

        data = self.python_file.extractClasses(data)

        self.assertTrue(len(self.python_file._classes) == number_class)
        for stored_class in self.python_file._classes:
            self.assertTrue(type(stored_class) == html_gen.PythonClass)


    def test_extractImports(self, number_imports=5):
        """ Object method.
            Params: number_import (int) -> the import's number in the tested file.
            Return: None
            This method tests the behaviour of the extractImports method.
            The list _imported_modules is initialize with an empty list.
            extractImports is called on the content of the tested file.
            The length of the _imported_modules list needs to be equal to the number_imports param.
        """

        self.python_file._imported_modules = []
        with open(__file__, "r") as file_resource:
            data = file_resource.read()

        data = self.python_file.extractImports(data)
        
        self.assertTrue(len(self.python_file._imported_modules) == number_imports)
        for stored_imports in self.python_file._imported_modules:
            self.assertTrue(type(stored_imports) == str)


    def test_sort(self):
        """ Object method.
            Params: None
            Return: None
            This method tests the behaviour of the sort Method.
            It calls sort and verifies that the classes list is sorted by alphabetic order.
        """
        self.python_file.sort()
        i = 1
        while i<len(self.python_file._classes):
            self.assertTrue(self.python_file._classes[i]._name >= self.python_file._classes[i-1]._name)
            i+=1




class TestPythonClass(unittest.TestCase):
    """ Inherits: unittest.TestCase
        This class tests the behaviour of each method of the class PythonClass.
    """

    def setUp(self):
        """ Object method.
            Params: None
            Return: None
            Method called before each test, initializing it.
            A python_class attribute, PythonClass's object is added for tests all the method of this class.
            The content gave to the attributes is the first class of the current file.
        """
        with open(__file__, "r") as file_resource:
            data = file_resource.read()

        result = re.search(REGEX_CLASS, data, flags=re.DOTALL)
        self.python_class = html_gen.PythonClass(result.group("name"),result.group("docstring"),result.group("methods"))

    def test_extractContent(self, number_method=2):
        """ Object method
            Params: number_method (int) -> the method's number of the tested class.
            Return: None
            This method tests the behaviour of the extractContent method.
            The list _methods is initialize with an empty list.
            extractContent is called on the tested class. 
            The length of the _methods list needs to be equal to the number_method param.
        """
        self.python_class._methods = []
        with open(__file__, "r") as file_resource:
            data = file_resource.read()
        result = re.search(REGEX_CLASS, data, re.DOTALL)

        data = self.python_class.extractContent(result.group("methods"))
        
        self.assertTrue(len(self.python_class._methods) == number_method)
        for method in self.python_class._methods:
            self.assertTrue(type(method) == html_gen.PythonMethod)


    def test_sort(self):
        """ Object method
            Params: None
            Return: None
            This method tests the behaviour of the sort method.
            It calls sort and verifies that the _methods list is sorted by alphabetic order.
        """
        self.python_class.sort()
        i = 1
        while i<len(self.python_class._methods):
            self.assertTrue(self.python_class._methods[i]._name >= self.python_class._methods[i-1]._name)
            i+=1


if __name__ == "__main__":
    unittest.main()