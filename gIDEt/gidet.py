from gi.repository import GObject, Gtk, Gedit, Gio
import projects
import os
import iconmanager

class GIDEt(GObject.Object, Gedit.WindowActivatable):
    
    __gtype_name__ = "gIDEt"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
        
    def do_activate(self):
        
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
        
        self._treeview = Gtk.TreeView.new_with_model(self.get_tree_store())
        
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
    
    def get_tree_store(self):
        tree_store = Gtk.TreeStore(GObject.TYPE_STRING,    # icon
                                        GObject.TYPE_STRING,    # name
                                        GObject.TYPE_STRING)    # uri
        for project in projects.all_projects2():
            project_tree =  tree_store.append( None,  \
                [project.icon, project.name, project.uri] )

            self.add_nodes_to_project(project.uri, tree_store, project_tree)
        return tree_store

#TODO se puede llegar hacer que el proyecto conozca sus packages y ellos 
#los files, pero no lo llegue hacer
    def add_nodes_to_project(self, uri, tree_store, project_tree):
        parents = {}
        for dir, dirs, files in os.walk(uri):
            for subdir in dirs:
                parents[os.path.join(dir, subdir)] =  \
                    tree_store.append(parents.get(dir, project_tree), \
                        [iconmanager.get_package_icon(), subdir, "dir"])

            for item in files:
                tree_store.append(parents.get(dir, project_tree),  \
                    [iconmanager.get_file_icon(item), item,  \
                        os.path.join(dir, item)])        
            
    def _open_selected_file(self, treeview, path, tree_column):
        (model, treeiter) = treeview.get_selection().get_selected()
        uri = model.get_value(treeiter, 2)

        if(os.path.isfile(uri)):
            location  = Gio.file_new_for_uri(uri)
            tab = self.window.get_tab_from_location(location)
            if tab:
                self.window.set_active_tab(tab)
            else:
                self.window.create_tab_from_uri(uri, None, 0, 0, False, True)

        print "uri " + str(uri)

        # TODO abrir archivo
        # Gedit.Document.load(gio.File(model.get_value(treeiter, 1)))
