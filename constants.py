
""" Module containing all the constants used in the GooDoc project. """


################################################################## DOCUMENTATION ################################################################## 

######## HTML GENERATION ########

# REGULAR EXPRESSION

REGEX_CLASS = r'class (?P<name>[\w ]+(\(.*?\))?):\s+'\
              + r'("{3}(?P<docstring>.+?)"{3})?\s+'\
              + r'(?P<methods>def [\w]+\(.*?\):\s+'\
              + r'("{3}(.+?)"{3})?\s+'\
              + r'.+?)((\n(\w|$))|$)'

REGEX_METHOD = r'def (?P<name>[\w ]+\(.*?\)):\s+'\
               + r'("{3}(?P<docstring>.+?)"{3})?\s+'

REGEX_DOCSTRING = r'"{3}(?P<docstring>.+?)"{3}\s+'

REGEX_IMPORT = r'\nimport (?P<module>.+)\n'
REGEX_IMPORT_FROM = r'\nfrom (?P<lib>.+) import (?P<element>.+)\n'

REGEX_STYLE = r'href=(?P<style>.+?) '

# INDENTATION LEVEL

FILE_INDENTATION_LEVEL = 3
CLASS_INDENTATION_LEVEL = 4
METHOD_INDENTATION_LEVEL = 6

# File name
JAVASCRIPT_FILE_PATH = "./javascript/fold.js"

# ELEMENTS ORDER

NATURAL_ORDER = "natural_order"
ALPHABETICAL_ORDER = "alphabetical_order"

######## SCREEN ########

# Title
DOCUMENTATION_TITLE = "GooDoc - Documentation"
STYLE_BUTTON_TITLE = "Stylesheets"

# Images
ADD_FILES_ICON = "img/addFiles.png"
ADD_DIR_ICON = "img/addDir.png"
START_ICON = "img/start.png"
SETTINGS_ICON = "img/settings.png"

# Shortcuts
ADD_FILES_SHORTCUT = 'Ctrl+O'
ADD_DIR_SHORTCUT = 'Ctrl+Shift+O'
START_SHORTCUT = 'Ctrl+K'
SETTINGS_SHORTCUT = 'Ctrl+L'

# ToolTip
ADD_FILES_TIP = "Add files"
ADD_DIR_TIP = "Add directory"
START_TIP = "Start generation"
SETTINGS_TIP = "Settings"

# Folders
NAME_CREATED_FOLDER = "GOODOC_DOCUMENTATION"

# Style sheet
DOCSCREEN_STYLESHEET_PATH = "./style/documentation_screen.css"

# Extension
AUTHORIZED_EXTENSIONS = (".py",".pyw",".htm",".html")

######## TBD ########

DEFAULT_FILE_SELECT_LOCATION = "C:\\"

################################################################## STYLESHEETS ################################################################## 

# Title Screen
STYLE_TITLE = "GooDoc - Stylesheets"

# Style path
STYLE_GOO_PATH = "./style/goo.css"
STYLE_DEEPBLUE_PATH = "./style/deepblue.css"
STYLE_MELTDOWN_PATH = "./style/meltdown.css"
STYLE_DOXYGEN_PATH = "./style/doxygen.css"

# Style name
STYLE_GOO_NAME = "Goo"
STYLE_DEEPBLUE_NAME = "Deep Blue"
STYLE_MELTDOWN_NAME = "Meltdown"
STYLE_DOXYGEN_NAME = "Doxygen"
NEW_STYLE_NAME = "NewStyle"

# Other path
SAVE_FILE_PATH = "./save/saved_style"
SAVE_FOLDER_PATH = "./save"
STYLE_BASENAME = "'(GOODOC_STYLE_BASENAME)'"
STYLESCREEN_STYLESHEET_PATH = "./style/style_screen.css"

# Other name
CONFIRM_BUTTON_NAME = "Choose"
