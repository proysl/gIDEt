from gi.repository import GObject, Gtk, Gedit
import gio
from Workspace import Workspace

class GIDEt(GObject.Object, Gedit.WindowActivatable):
    
    __gtype_name__ = "gIDEt"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
        
    def do_activate(self):
        self._workspace = Workspace()
        
        icon = Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU)
        panel = self.window.get_side_panel()
        
        column = Gtk.TreeViewColumn()
        column.set_title("gIDEt")
        
        cell = Gtk.CellRendererPixbuf()
        column.pack_start(cell, False)
        
        column.add_attribute(cell, "stock-id", 0)
        
        cell = Gtk.CellRendererText()
        column.pack_start(cell, True)
        column.add_attribute(cell, "text", 1)
        
        self._treeview = Gtk.TreeView.new_with_model(self._workspace.get_treestore())
        
        self._treeview.set_tooltip_column(2)
        self._treeview.append_column(column)
        
        # Basic open event
        self._treeview.connect("row-activated", self._open_selected_file)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self._treeview)
        
        #El escroll tienen q estar en un Box (VBox o HBox)
        self._panel_widget = Gtk.VBox(homogeneous=False, spacing=2)
        self._panel_widget.pack_start(scrolled, True, True, 0)
        self._panel_widget.show_all()
        
        # add the panel
        panel.add_item(self._panel_widget, "gIDEt", "gIDEt", icon)
    
    def do_deactivate(self):
        self.window.get_side_panel().remove_item(self._panel_widget)
    
    def do_update_state(self):
        pass
    
    ### PRIVATE ###
    
    def _open_selected_file(self, treeview, path, tree_column):
        (model, treeiter) = treeview.get_selection().get_selected()
        print model.get_value(treeiter, 1)
        # TODO abrir archivo
        # Gedit.Document.load(model.get_value(treeiter, 1))
