from gi.repository import Gtk

file_icons = { \
    "py"   : Gtk.STOCK_EDIT,
    "java" : Gtk.STOCK_EDIT,
    "cpp"  : Gtk.STOCK_EDIT,
    "c"    : Gtk.STOCK_EDIT
}
project_icons = {\
    "python" : Gtk.STOCK_OPEN,
    "java"   : Gtk.STOCK_OPEN,
    "c++"    : Gtk.STOCK_OPEN,
    "c"      : Gtk.STOCK_OPEN
}
    
def get_file_icon(file_name):
    extension = file_name.split(".")[1]
    if extension in file_icons.keys():
      return file_icons[extension]
    else:
      return default_icon()
          
def get_project_icon(language):
    if language in project_icons:
        return project_icons[language]
    else:
        return default_project_icon()

def get_package_icon():
    return Gtk.STOCK_HELP
    
def default_icon():
    return Gtk.STOCK_DND

def default_project_icon():
    return Gtk.STOCK_DND
