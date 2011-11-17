class Workspace:
	
	def __init__(self):
		self.uri = None
		
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
