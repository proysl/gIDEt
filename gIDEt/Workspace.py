import os
from Tree import *

class Workspace:
	
    def __init__(self, uri):
        self.uri = uri
        self.tree = None

    def init(self):
        self.tree = Tree()
        parents = {}
        for dir, dirs, files in os.walk(self.uri):
            for subdir in dirs:
                parents[os.path.join(dir, subdir)] = self.tree.appendNode(parents.get(dir, None), subdir)
            for item in files:
                self.tree.appendNode(parents.get(dir, None), item)
                print str(parents.get(dir, None)) + ' - ' + str(item)

	def get_uri(self):
		return self.uri

		
	def create_project(self, project):
		# generar carpeta con el nombre del project
		# crear .project (o similar) con la metadata
		pass
		
	def get_projects(self):
		# busca en la carpeta del workspace
		# aquellas carpetas que tengan .project
		# y las retorna como objetos Projects
		pass
