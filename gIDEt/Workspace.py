import os
from gi.repository import Gtk, GObject
from IconAssignator import IconAssignator

class Workspace:
    
    # TODO pegarle a GSettings o a archivo de configuracion
    GIDET_PROJECT_CONF_FILE = ".project"
    DEFAULT_WORKSPACE_PATH = os.path.expanduser("~") + "/.gIDEt/workspace"
    
    def __init__(self, uri=None):
        if uri is None:
            self._uri = self.DEFAULT_WORKSPACE_PATH
        else:
            self._uri = uri
        self._icon_assignator = IconAssignator()
        self._init_treestore()
    
    def get_uri(self):
        return self._uri
    
    def get_treestore(self):
        return self._treestore
    
    def get_icon_assignator(self):
        return self._icon_assignator
    
    def create_project(self, project):
        # generar carpeta con el nombre del project
        # crear .project (o similar) con la metadata
        pass
    
    def get_projects(self):
        # busca en la carpeta del workspace
        # aquellas carpetas que tengan .project
        # y las retorna como objetos Projects
        pass
    
    ### PRIVATE ###
    
    def _init_treestore(self):
        self._treestore = Gtk.TreeStore(GObject.TYPE_STRING,    # icon
                                        GObject.TYPE_STRING,    # name
                                        GObject.TYPE_STRING)    # uri
        parents = {}
        for directory, dirs, files in os.walk(self.get_uri()):
            for subdir in dirs:
                self._add_dir_if_project(parents, directory, subdir)
            for item in files:
                self._treestore.append( \
                    parents.get(directory, None),
                    [self.get_icon_assignator().get_icon_from_file(item),
                    item, "uri"])
    
    def _add_dir_if_project(self, parents, directory, subdir):
        if self._has_project(subdir):
            parents[os.path.join(directory, subdir)] = \
                self._treestore.append( \
                    parents.get(directory, None),
                    [Gtk.STOCK_OPEN, subdir, "dir"]
                )
    
    def _has_project(self, directory):
        for file_name in os.listdir(self.get_uri() + '/' + directory):
            if file_name == self.GIDET_PROJECT_CONF_FILE: return True
        return False
