from gi.repository import  Gtk

class IconAssignator:
    
    def __init__(self):
        self._types = {"py"   : Gtk.STOCK_EDIT,
                       "java" : Gtk.STOCK_EDIT,
                       "cpp"  : Gtk.STOCK_CANCEL,
                       "c"    : Gtk.STOCK_CANCEL}
    
    def get_icon_from_file(self, file_name):
      extension = file_name.split(".")[1]
      if extension in self._types.keys():
          return self._types[extension]
      else:
          return self._default_icon()
    
    ### PRIVATE ###
    
    def _default_icon(self):
        return Gtk.STOCK_DND
