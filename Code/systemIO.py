import stdlib
import os
import os.path


class FileSystemInfo(object):

    def __init__(self, path, parent = None, typ = stdlib.FILE):
        '''(FileSystemInfo, string[, FileSystemInfo, int]) -> NoneType

        Construct a file inforamtion from given path

        self : the file
        path : the path of the file
        parent : parent of the file
        typ : indicating whether it is a directory or a file
        '''

        self.display_unit = None
        self.parent = parent
        self.path = path
        self.next = None
        self.previous = None
        self.typ = typ
        if typ == stdlib.FILE:
            self.size = os.path.getsize(path)

    def __cmp__(self, other):
        '''(FileSystemInfo, FileSystemInfo) -> int

        Compare the size of the file
        Return 1 if size of self is larger than that of other
        Return -1 if size of self is smalle than that of other
        Return -1 if size of self is equal to that of other

        self : the file
        other : the other file
        '''

        if self.size < other.size:
            return -1
        elif self.size > other.size:
            return 1
        else:
            return 0


class DirectoryInfo(FileSystemInfo):

    def __init__(self, path, parent = None):
        '''(DirectoryInfo, string, DirectoryInfo) -> NoneType

        Construct a directory inforamtion from given path

        self : the folder
        path : the path of the folder
        parent : parent of the folder
        '''

        FileSystemInfo.__init__(self, path, parent, stdlib.DIRECTORY)
        self.children = []
        self.size = 0
        # get all children
        for filename in os.listdir(path):
            subitem = os.path.join(path, filename)
            file_info = None
            if os.path.isdir(subitem):
                # get all the sub-directory
                file_info = DirectoryInfo(subitem, self)
            else:
                # get all the files
                file_info = FileSystemInfo(subitem, self)
            self.size += file_info.size
            self.children.append(file_info)
        # put all the children in order and connect them
        self.children.sort()
        self.connect_children()

    def connect_children(self):
        '''(DirectoryInfo) -> NoneType

        Connect all the children of the directory

        self : the folder
        '''

        # connect all the children
        # from 1 to n-2
        for i in range(1, len(self.children) - 1):
            self.children[i].next = self.children[i + 1]
            self.children[i + 1].previous = self.children[i]
        if len(self.children) > 1:
            # connect 0 and 1 if more than 2 children
            self.children[0].next = self.children[1]
            self.children[1].previous = self.children[0]
            # connect n-1 and 0
            self.children[len(self.children) - 1].next = self.children[0]
            self.children[0].previous = self.children[len(self.children) - 1]
