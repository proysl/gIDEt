from gi.repository import GObject, Gtk, Gedit

class GIDEt(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "gIDEt"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
        
    def do_activate(self):
        icon = Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU)
        panel = self.window.get_side_panel()
        self._store = Gtk.TreeStore(GObject.TYPE_STRING,    # icon
                                    GObject.TYPE_STRING,    # name
                                    GObject.TYPE_STRING,    # uri
                                    GObject.TYPE_INT)       # editable 

        # create the treeview
        self._treeview = Gtk.TreeView.new_with_model(self._store)
        panel.activate_item(self._treeview)
        panel.add_item(self._treeview, "WorkspaceExplorer", "Workspace Explorer", icon)

    def do_deactivate(self):
        panel = self.window.get_side_panel()
        panel.remove_item(self._side_widget)

    def do_update_state(self):
        pass
