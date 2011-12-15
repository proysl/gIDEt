import Tkinter, tkFileDialog
import os



class FileManager():

    def __init__(self):
        root = Tkinter.Tk()
        root.withdraw()
        self.dir_opt = options = {}
        options['initialdir'] = '~'
        options['mustexist'] = False
        options['parent'] = None
        options['title'] = 'This is a title'
        options['parent'] = root

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = ''
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = '~'
        options['initialfile'] = ''
        options['parent'] = root
        options['title'] = 'This is a title'

    def askdirectory(self):
        return tkFileDialog.askdirectory(**self.dir_opt)

    def asksavefilename(self, uri):   
        self.file_opt["initialdir"] = uri
        return tkFileDialog.asksaveasfile(mode='w', **self.file_opt)

    def remove_url(self, uri):
        cmd_rm= "rm -rf "+uri
        os.system(cmd_rm)
            

    def mkdir_to_path(self, path):
        self.dir_opt["initialdir"] = path
        os.mkdir(self.askdirectory())
 






