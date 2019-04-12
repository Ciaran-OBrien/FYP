class FileUp(object):
    """docstring forFileUp."""
    def __init__(self):
        self.check = False
        self.filePath = ""
        self.fileName = ""

    def set_check(self,status):
        self.check = status

    def set_filePath(self,filePath):
        self.filePath = filePath

    def set_fileName(self,fileName):
        self.fileName = fileName

    def get_check(self):
        return self.check

    def get_filePath(self):
        return self.filePath

    def get_fileName(self):
        return self.fileName
