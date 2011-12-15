import os
import ConfigParser as configparser
import iconmanager

DEFAULT_WORKSPACE_PATH = os.path.expanduser("~") + "/.gIDEt/workspace"

PROJECT_SECTION = "project"
LANGUAGE_SECTION = "language"
PROJECT_NAME_OPTION = "name"
PROJECT_LANGUAGE_OPTION = "language"
GIDET_PROJECT_CONF_FILE = ".project"
WORKSPACE_CONF_FILE = ".workspace"

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
        
def new_project(project_name, language, project_uri):
#    full_uri = os.path.join(workspace_uri, project_name)
    # create directory and .project file with its data
    os.mkdir(project_uri)
    os.chdir(project_uri)
    project_file = open(GIDET_PROJECT_CONF_FILE, "wr")
    config_file = configparser.ConfigParser()
    config_file.add_section(PROJECT_SECTION)
    config_file.set(PROJECT_SECTION, PROJECT_NAME_OPTION, project_name)
    config_file.add_section(LANGUAGE_SECTION)
    config_file.set(LANGUAGE_SECTION, PROJECT_LANGUAGE_OPTION, language)
    config_file.write(project_file)
    project_file.close()

    #guarda en la configuracion del worksace, la referencia al nuevo projecto
    os.chdir(DEFAULT_WORKSPACE_PATH)
    workspace_config_file = open(WORKSPACE_CONF_FILE, "a+b")
    workspace_config_file.write(project_uri + "\n")
    workspace_config_file.close 

    # create the project object and return it
    return Project(project_uri, project_name, language)

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



def all_projects2():
    os.chdir(DEFAULT_WORKSPACE_PATH)
    config = open(WORKSPACE_CONF_FILE, "a+b")

    projects = [load_project_from_file(project_dir) \
            for project_dir \
            in [path_project[:-1] \
                for path_project \
                in config.readlines() \
                if isdir(path_project)]
            if contains_project(project_dir)]

    config.close()
    return projects

def isdir(path):
    return os.path.isdir(path[:-1])


def all_projects():
    return [load_project_from_file(project_dir) \
            for project_dir \
            in [os.path.join(workspace_uri, subdir) \
                for subdir \
                in os.listdir(workspace_uri) \
                if os.path.isdir(os.path.join(workspace_uri, subdir))]
            if contains_project(project_dir)]



