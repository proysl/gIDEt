import os
import ConfigParser as configparser
import iconmanager

DEFAULT_WORKSPACE_PATH = os.path.expanduser("~") + "/.gIDEt/workspace"

PROJECT_SECTION = "project"
LANGUAGE_SECTION = "language"
PROJECT_NAME_OPTION = "name"
PROJECT_LANGUAGE_OPTION = "language"
GIDET_PROJECT_CONF_FILE = ".project"

workspace_uri = DEFAULT_WORKSPACE_PATH

class Project:
    
    def __init__(self, uri, name, language):
        self.uri = uri
        self.name = name
        self.language = language
        self.icon = iconmanager.get_project_icon(language)
        # TODO It would be nice to add something like
        # self.common_file_templates = template_manager.templates_for(language)
        # to get a list of templates for a project, like
        # Java Class, Java Interface, Python class, Python empty module, Django class and so on
        
def new_project(project_name, language, workspace_uri):
    full_uri = os.path.join(project, project_name)
    # create directory and .project file with its data
    os.mkdir(full_uri)
    config_file = configparser.ConfigParser().readfp(project_file)
    config_file.add_section(PROJECT_SECTION)
    config_file.set(PROJECT_SECTION, PROJECT_NAME_OPTION, project_name)
    config_file.add_section(LANGUAGE_SECTION)
    config_file.set(LANGUAGE_SECTION, PROJECT_LANGUAGE_OPTION, language)
    project_file = open(os.path.join(full_uri, GIDET_PROJECT_CONF_FILE), "w")
    config.write(project_file)
    project_file.close()
    # create the project object and return it
    return Project(full_uri, project_name, language)
    
def load_project_from_file(full_uri):
    project_file = open(os.path.join(full_uri, GIDET_PROJECT_CONF_FILE), "r")
    config_file = configparser.ConfigParser()
    config_file.readfp(project_file)
    project_name = config_file.get(PROJECT_SECTION, PROJECT_NAME_OPTION)
    project_language = config_file.get(LANGUAGE_SECTION, PROJECT_LANGUAGE_OPTION)
    project_file.close()
    return Project(full_uri, project_name, project_language)
    
def contains_project(uri):
    return any(file_name == GIDET_PROJECT_CONF_FILE \
            for file_name in os.listdir(uri))

def all_projects():
    return [load_project_from_file(project_dir) \
            for project_dir \
            in [os.path.join(workspace_uri, subdir) \
                for subdir \
                in os.listdir(workspace_uri) \
                if os.path.isdir(os.path.join(workspace_uri, subdir))]
            if contains_project(project_dir)]
