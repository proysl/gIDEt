from Project import *
from Workspace import *

class ProjectManager:

	def __init__(self):
		self.workspace = None
		self.projects = None
		
	def get_projects(self):
		return self.projects
	
	def create_project(self, project):
		self.workspace.create_project(project)
		self.project.add(project)
		
	
