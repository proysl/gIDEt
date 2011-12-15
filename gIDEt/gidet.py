from gi.repository import GObject, Gtk, Gedit, Gio, Gdk
import projects
import os
import iconmanager
from filemanager import *



# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
        <menu action="None">
            <placeholder name="New Proyects">
                <menuitem name="a" action="newJavaProject"/>
                <menuitem name="b" action="newPythonProject"/>
                <menuitem name="c" action="newHaskellProject"/>
            </placeholder>
        </menu>
    </menu>
  </menubar>
</ui>
"""


class GIDEt(GObject.Object, Gedit.WindowActivatable):
    
    __gtype_name__ = "gIDEt"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
        self._uri_selected = None
        self.tree_store = None
        self.file_manager = FileManager()
        self.menu = Gtk.Menu()
        new_file = Gtk.MenuItem("Nuevo Archivo")
        new_folder = Gtk.MenuItem("Nuevo directorio")
        remove = Gtk.MenuItem("Eliminar")

        new_file.connect("activate", self.on_new_file)
        new_folder.connect("activate", self.on_new_folder)
        remove.connect("activate", self.on_remove)

        # Agregar los items al menu
        self.menu.append(new_file)
        self.menu.append(new_folder)
        self.menu.append(remove)
        self.menu.show_all()


    def do_activate(self):
        self._insert_menu()
        
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
        self._treeview.connect('button-press-event', self.open_menu)
        
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
        # Remove any installed menu items
        self._remove_menu()

    

    def open_menu(self, widget, event):
        (model, treeiter) = self._treeview.get_selection().get_selected()
        self._uri_selected = model.get_value(treeiter, 2)
        if(event.button == 3):
            self.menu.popup_for_device(None, None, None, Gtk.StatusIcon.position_menu,  event.button, event.time, Gtk.get_current_event_time())

    
    ### PRIVATE ###

###################################################3

    def _insert_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()
        # Create a new action group
        self._action_group = Gtk.ActionGroup("GIDETPluginActions")


        self._action_group.add_actions([('newJavaProject', None, 'new Java Project', None,'new Java Project', self.on_new_java_project), \
            ('newPythonProject', None, 'new Python Project', None,'new Python Project', self.on_new_python_project), \
            ('newHaskellProject', None, 'new Haskell Project', None,'new Haskell Project', self.on_new_haskell_project),
            ('None', None, 'New Project', None,'new Project', None)])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def do_update_state(self):
        self._action_group.set_sensitive(self.window.get_active_document() != None)
        #self.load_all_projects()

    def on_new_java_project(self, action):
        path = self.file_manager.askdirectory()
        project_name = self.get_project_name_to_path(path)
        self.update_new_project(projects.new_project(project_name, "java",path))


    def on_new_python_project(self, action):
        path = self.file_manager.askdirectory()
        project_name = self.get_project_name_to_path(path)
        self.update_new_project(projects.new_project(project_name, "python", path))

    def on_new_haskell_project(self, action):
        path = self.file_manager.askdirectory()
        project_name = self.get_project_name_to_path(path)
        self.update_new_project(projects.new_project(project_name, "haskell",path))

    def update_new_project(self, project):
#        self.load_all_projects()
        project_tree = self.tree_store.append( None,  \
                [project.icon, project.name, project.uri] )
        self.add_nodes_to_project(project.uri, self.tree_store, project_tree)

    def get_project_name_to_path(self, path):
        split = path.split("/") 
        return split[len(split)-1]

    def on_new_file(self, a, **b):
        self.file_manager.asksavefilename(self._uri_selected)
        self.load_all_projects() #TODO actualizar solo ese proyecto

    def on_new_folder(self, a, **b):
        self.file_manager.mkdir_to_path(self._uri_selected)
        self.load_all_projects() #TODO actualizar solo ese proyecto

    def on_remove(self, a, **b):
        self.file_manager.remove_url(self._uri_selected)
        self.load_all_projects() #TODO actualizar solo ese proyecto
        

######################################3333

    def get_tree_store(self):
        self.tree_store = Gtk.TreeStore(GObject.TYPE_STRING,    # icon
                                        GObject.TYPE_STRING,    # name
                                        GObject.TYPE_STRING)    # uri
        self.load_all_projects()
        return self.tree_store

    def load_all_projects(self):
        self.tree_store.clear()
        for project in projects.all_projects2():
            project_tree =  self.tree_store.append( None,  \
                [project.icon, project.name, project.uri] )

            self.add_nodes_to_project(project.uri, self.tree_store, project_tree)

#TODO se puede llegar hacer que el proyecto conozca sus packages y ellos 
#los files, pero no lo llegue hacer
    def add_nodes_to_project(self, uri, tree_store, project_tree):
        parents = {}
        for dir, dirs, files in os.walk(uri):
            for subdir in dirs:
                parents[os.path.join(dir, subdir)] =  \
                    tree_store.append(parents.get(dir, project_tree), \
                        [iconmanager.get_package_icon(), subdir, os.path.join(dir, subdir) ])

            for item in files:
                if(item[0] == "."):
                    continue
                tree_store.append(parents.get(dir, project_tree),  \
                    [iconmanager.get_file_icon(item), item,  \
                        os.path.join(dir, item)])        
            
    def _open_selected_file(self, treeview, path, tree_column):
        (model, treeiter) = treeview.get_selection().get_selected()
        uri = model.get_value(treeiter, 2)

        if(os.path.isfile(uri)):
#            Gedit.Document.load(Gio.file_new_for_uri(uri))
            location  = Gio.file_new_for_uri(uri)
            tab = self.window.get_tab_from_location(location)
            if tab:
                self.window.set_active_tab(tab)
            else:
			    self.window.create_tab_from_location(location, None, 0, 0, False, True)
                #self.window.create_tab_from_uri(uri, None, 0, 0, False, True)

        print "uri " + str(uri)

        # TODO abrir archivo
        # Gedit.Document.load(gio.File(model.get_value(treeiter, 1)))
