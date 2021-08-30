"""
Here I will figure out cute download and extraction methods for models to make it easier on my users.



"""

import urllib.request
urlname="https://github.com/blue-fish/Real-Time-Voice-Cloning/releases/download/v1.0/pretrained.zip"
with urllib.request.urlopen(urlname) as f:
    with open(urlname.split('/')[-1],'ab') as myfile:
        myfile.write(f.read())


import zipfile
with zipfile.ZipFile("pretrained.zip", 'r') as zip_ref:
    zip_ref.extractall('./')

#so now I can download and extract the files... lets make a function which
#can determine the installation location of the installed voice cloner software
#and then extracts the files to it.
#https://stackoverflow.com/questions/247770/how-to-retrieve-a-modules-path
#https://stackoverflow.com/questions/3811197/getting-admin-password-while-copy-file-using-shutil-copy
#https://www.geeksforgeeks.org/python-shutil-copytree-method/

def getModulePath(modulename):
    import os
    import inspect
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))#this should be the location of the currently executing file -- which means if placed in the right location could tell the location of everything else.
