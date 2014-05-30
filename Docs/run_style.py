import Tkinter
from tkFileDialog import askopenfilename
import sys
import os
import os.path
import pep8


if __name__ == "__main__":
    root = Tkinter.Tk()
    d = "E:\Course\CSC\CSC148\Assignment\A2\Work\Code"
    for item in os.listdir(d):
        subitem = os.path.join(d, item)
        if not os.path.isdir(subitem) and subitem.endswith(".py"):
            py_file  = subitem
            pep8.process_options(['-v', '--count', py_file])
            pep8.input_file(py_file)
            if pep8.get_statistics() == []:
                print "Congrats! No style errors were detected."
