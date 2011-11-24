from  ReadProperties import *
reader = ReadProperties()
reader.read("/home/nny/Dropbox/PenDrive/plugins/gedit/plugins/gIDEt/.properties")
print reader.getProjectType()

from Workspace import *

w = Workspace("./")
w.init()
print w.tree

