#!/usr/bin/python3
#-*- coding:utf-8 -*-

""" Module modeling all the Python elements used in the GooDoc Project.

    It contains four classes:
        - PythonElement: Superclass of all python elements.
        - PythonFile : Data structure representing a Python file
        - PythonClass : Data structure representing a Python class, inside a file
        - PythonMethod : Data structure representing a Python method, inside a Python class
"""

import os
import re
import sys
from constants import *


class PythonElement:
    """ Inherits: None
        This class represents an abstract block of Python code. It must be subclassed.
        It has one attribute, _name, and a method initDocstring.
    """

    def __init__(self, name):  
        """ Constructor
            Param: String name -> the name of the python element
            Return: None
            Initializes the attribute _name with the name given in params 
        """
        self._name = name

    def initDocstring(self, docstring, indentation_level):
        """ Object method
            Params: String docstring -> the docstring to initialize
                    int indentation_level -> the indentation level to add to the docstring
            This method initializes and formats the element's docstring
            It splits the docstring into a list of lines. Each line is stripped of its leading and tailing whitespaces.
            The list of lines is then joined with '<br />' tags and appropriately indented.
        """
        if docstring == None:
            self._docstring = ""
            return 

        array_line = docstring.split("\n")

        i = 0
        length = len(array_line)
        while i<length:
            array_line[i] = array_line[i].strip()
            i+=1

        sep = "<br />\n"+"\t"*indentation_level
        self._docstring = sep.join(array_line)




class PythonFile(PythonElement):
    """ Inherits: PythonElement.
        This class represents a source file, written in Python. 
    """

    def __init__(self, path):
        """ Constructor
            Params: String path -> the python file's path
            Return: None
            The content of the path's file is backed up
            The _name attribute is the given path, without its extension.
            The _classes attributes is an empty list, initialized with the extractContent method.
        """
        with open(path, "r") as file_resource:
            data = file_resource.read()

        super().__init__(os.path.splitext(path)[0])
        self._classes = []
        self._imported_modules = []
        self.extractContent(data)


    def extractContent(self, data):
        """ Object method
            Params: String data -> file's content.
            Return: None
            The docstring content is sent to the initDocstring method.
            From the given content, the _classes list is filled, using the extractClasses method.
            Then the _imports list is initialized, by calling the extractImports method.
        """
        # Docstring initialization
        result = re.search(REGEX_DOCSTRING, data, re.DOTALL)
        if result != None:
            docstring = result.group("docstring")
        else:
            docstring = ""
        self.initDocstring(docstring, FILE_INDENTATION_LEVEL)

        # Classes list creation
        data = self.extractClasses(data)

        # importations list creation
        data = self.extractImports(data)

    def extractClasses(self, data):
        """ Object method.
            Params: String data -> the file's content
            Return: the rest of the file's content (String)
            This method extracts the python classes contained in the data param, and fills the _classes list.
            For each class, a PythonClass object is created and appended to the _classes list.
        """
        class_regex = re.compile(REGEX_CLASS, re.DOTALL)
        result = class_regex.search(data)

        while result is not None:
            new_class = PythonClass(result.group("name"), result.group("docstring"), result.group("methods"))
            self._classes.append(new_class)
            data = data[0:result.start()] + data[result.end()-1:]
            result = class_regex.search(data)

        return data

    def extractImports(self, data):
        """ Object method
            Params: String data -> the file's content
            Return: the rest of file's content (String)
            This method extracts the python imports contained in the data param, and fills the _imported_modules list.
            For each line, the name of the imported module is added to the _imported_modules list.
        """

        imports_regex = re.compile(REGEX_IMPORT)
        result = imports_regex.search(data)

        while result is not None:
            self._imported_modules.append(result.group("module"))
            data = data[0:result.start()] + data[result.end()-1:]
            result = imports_regex.search(data)

        importfrom_regex = re.compile(REGEX_IMPORT_FROM)
        result = importfrom_regex.search(data)

        while result is not None:
            self._imported_modules.append(result.group("lib")+"."+result.group("element"))
            data = data[0:result.start()] + data[result.end()-1:]
            result = importfrom_regex.search(data)

        return data


    def save(self, path, order = NATURAL_ORDER):
        """ Object method
            Params: String order -> the order of methods and classes (natural or alphabetical) in the documentation, has NATURAL_ORDER constant for default value
                    String path -> the save folder's path
            Return: The new path of the generated file (String)
            This method generates html documentation of the current file, and saves it in a new file. 
            This file has the name of the current file, with a '.html' extension.
            May call the sort() method.
        """
        
        if order == ALPHABETICAL_ORDER:
            self.sort()

        new_path = os.path.join(path, os.path.basename(self._name) + ".html")
        
        with open(new_path, "w") as file_resource:
            file_resource.write(self.document())

        return new_path

    def sort(self):
        """ Object method
            Params: None
            Return: None
            Each class sorts its elements by alphabetical order. 
            Then self sorts its classes in the same way.
        """

        for python_class in self._classes:
            python_class.sort()

        self._classes.sort(key = lambda x: x._name)


    def document(self):
        """ Object method
            Params: None
            Return: documentation of the current file (String).
            This method generates the documentation of the PythonFile for which it is called by calling documentHead() and documentBody().
        """
        html_documentation = "<!DOCTYPE html>\n"
        html_documentation += "<html>\n"
        html_documentation += self.documentHead()
        html_documentation += self.documentBody()
        html_documentation += "</html>\n"
        return html_documentation


    def documentHead(self):
        """ Object method
            Params: None
            Return: html head of the current file (String)
            This method generates the html head of the current file.
        """
        html_head = "\t<head>\n"
        html_head += "\t\t<title> " + os.path.basename(self._name) + " </title>\n"
        html_head += "\t\t<meta charset='utf-8' />\n"
        html_head += "\t\t<link  rel='stylesheet' type='text/css' href=" + STYLE_BASENAME + " />\n"
        html_head += "\t\t<script src='" + os.path.basename(JAVASCRIPT_FILE_PATH) + "'></script>\n"
        html_head += "\t</head>\n"
        return html_head

    def documentBody(self):
        """ Object method.
            Params: None
            Return: html body of the current file (string).
            This method generates the html body of the current file.
        """
        # Title and docstirng
        html_body = "\t<body onload='foldAll();'>\n"
        html_body += "\t\t<h1>\n\t\t\t" + os.path.basename(self._name) + "\n\t\t</h1>\n"
        html_body += "\t\t<p>\n\t\t\t" + self._docstring + "\n\t\t</p>\n"
        html_body += "\t\t<h2>imports:</h2>\n\t\t<ul>\n"

        # Imports's documentation
        for element in self._imported_modules:
            html_body += "\t\t\t<li>"+element+"</li>\n"
        html_body += "\t\t</ul>\n"

        # Classes's documentation
        for python_class in self._classes:
            html_body += python_class.document()

        html_body += "\t</body>\n"
        return html_body



class PythonClass(PythonElement):
    """ Inherits: PythonElement
        This class represents a Python class.
    """

    def __init__(self, name, docstring, methods_content):
        """ Constructor
            Params: String name -> the class's name
                    String docstring -> the class's docstring
                    String methods_content -> the class's content.
            Return: None
            _name and _docstring attributes are initialized, by calling the super constructor and the initDocstring method.
            The _methods attributes is an empty list, initialized with the extractContent method.
        """
        super().__init__(name)
        self.initDocstring(docstring, CLASS_INDENTATION_LEVEL)
        self._methods = []
        self.extractContent(methods_content)


    def sort(self):
        """ Object method
            Params: None
            Return: None
            This method sort the _methods list by alphabetical order 
        """
        self._methods.sort(key=lambda x: x._name)


    def extractContent(self, data):
        """ Object method
            Params: String data -> the class's content
            Return: None
            With a regular expression, all the methods are extractes from the given content.
            For each method, a PythonMethod object is created and appended to the _methods list.
        """
        # List of methods creation
        method_regex = re.compile(REGEX_METHOD, re.DOTALL)
        result = method_regex.search(data)

        while result is not None:
            # Methods creation
            new_method = PythonMethod(result.group("name"), result.group("docstring"))
            self._methods.append(new_method)
            # Delete method from the class's content
            data = data[0:result.start()] + data[result.end():]
            result = method_regex.search(data)

    def document(self):
        """ Object method
            Params: None
            Return: the class's html documentation (String)
            This method generates the html_documentation of this Python Class, in an html section.
            This section contains the name of the class, its docstring and the documentation of all of its methods, in an html table.
        """
        html_documentation = "\t\t<section class='pythonClass'>\n"

        html_documentation += "\t\t\t<h2>\n\t\t\t\t" + self._name + "\n\t\t\t</h2>\n"
        html_documentation += "\t\t\t<p>\n\t\t\t\t" + self._docstring + "\n\t\t\t</p>\n"

        html_documentation += "\t\t\t<table class='methods'>\n"
        html_documentation += "\t\t\t\t<th colspan = 2> Methods </th>\n"

        for method in self._methods:
            html_documentation += method.document()

        html_documentation += "\t\t\t</table>\n"
        html_documentation +=  "\t\t</section>\n"
        return html_documentation




class PythonMethod(PythonElement):
    """ Inherits: PythonElement
        Class representing a Python method.
    """

    def __init__(self, name, docstring):
        """ Constructor
            Params: String name -> the method's name
                    String docstring -> the method's docstring.
            Return: None
            _name and _docstring attributes are initialized by calling super constructor and initDocstring method.
        """
        super().__init__(name)
        self.initDocstring(docstring, METHOD_INDENTATION_LEVEL)

    def document(self):
        """ Object method
            Params: None
            Return: the html documentation of this method (String).
            This method generates the html documentation of the PythonMethod for which it is called, on and html table's row.
            This row contains the name of the method, in the first cell and its formatted docstring in the second.
        """
        html_documentation = "\t\t\t\t<tr>\n"
        html_documentation += "\t\t\t\t\t<td onclick='toggle(this);'>\n\t\t\t\t\t\t" + self._name + "\n\t\t\t\t\t</td>\n"
        html_documentation += "\t\t\t\t\t<td>\n\t\t\t\t\t\t" + self._docstring + "\n\t\t\t\t\t</td>\n"
        html_documentation += "\t\t\t\t</tr>\n"
        return html_documentation


if __name__ == "__main__":
    files=[]

    order=ALPHABETICAL_ORDER
    for arg in sys.argv:
        if arg==ALPHABETICAL_ORDER or arg==NATURAL_ORDER:
            order=arg
        else:
            files.append(PythonFile(arg))

    for eachPythonFile in files:
        eachPythonFile.save(order)