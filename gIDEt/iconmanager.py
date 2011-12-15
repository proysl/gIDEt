from gi.repository import Gtk

file_icons = { \
    "py"   : Gtk.STOCK_EDIT,
    "java" : Gtk.STOCK_EDIT,
    "hs"   : Gtk.STOCK_EDIT,
    "cpp"  : Gtk.STOCK_EDIT,
    "c"    : Gtk.STOCK_EDIT,
    "."  : Gtk.STOCK_PROPERTIES
}
project_icons = {\
    "python" : Gtk.STOCK_HOME,
    "java"   : Gtk.STOCK_OPEN,
    "haskell": Gtk.STOCK_ABOUT,
    "c++"    : Gtk.STOCK_OPEN,
    "c"      : Gtk.STOCK_OPEN
}
    
def get_file_icon(file_name):
    if(file_name[0]=="."):
        return file_icons["."]
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
    return Gtk.STOCK_ADD
    
def default_icon():
    return Gtk.STOCK_DND

def default_project_icon():
    return Gtk.STOCK_DND
