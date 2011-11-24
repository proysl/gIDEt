from gi.repository import  Gtk

types = {"py":Gtk.STOCK_EDIT , "java":Gtk.STOCK_EDIT , "cpp":Gtk.STOCK_CANCEL , "c":Gtk.STOCK_CANCEL}

class IconAssignment:


	def __init__(self):
	    pass
		
	def getIconFromFile(self, aFile):
	    extencion = aFile.split(".")[1]
	    if extencion in types.keys():
  		return types[extencion]
	    else:
		return Gtk.STOCK_DND

	
	def get_language(self):
		return self.language
		
	
