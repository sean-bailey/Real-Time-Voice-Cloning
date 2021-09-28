"""

This file will be dedicated to make functions and/or classes to download and install the appropriate model sets and
put them in the default locations.

DEFAULT_ENCODER_PATH = "/encoder/saved_models/pretrained.pt"
DEFAULT_VOCODER_PATH = "/vocoder/saved_models/pretrained/pretrained.pt"
DEFAULT_SYNTHESIZER_PATH = "/synthesizer/saved_models/pretrained/pretrained.pt"

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
librosa.load(dir_path + "/samples/1320_00000.mp3")


Plan of action:

1) download zip file to library location
2) extract zip file in library location
3) move the contents of the encoder, vocoder and synthesizer directories inside the pretrained directory into
    the appropriate locations
4) delete the zip file and the extracted folder


We have a small problem: depending on the install location of the library (say, a user used sudo pip3 install .), we
may require elevated permissions to just download and install the files.

Here's how we're going to handle this for now:
1) Attempt to install to the known default locations.If successful, return these locations of installation.
2) If we run in to an error of "access denied" or similar, inform the user of this and then prompt them for their preferred
    installation location.
3) Attempt to download and install to this location. If the failure occurs, repeat 2.
4) Once properly downloaded and installed, return the location of the installed models.

TODO: find a way to have persistence in universal cases, i.e. somehow have the library know the updated default location between sessions.
"""
import errno
import os
import shutil
import zipfile

import requests
from tqdm import tqdm

installed_path = os.path.abspath(__file__)
installed_dir_path = os.path.dirname(installed_path)
installed_DEFAULT_ENCODER_PATH = installed_dir_path + "/encoder/"
installed_DEFAULT_VOCODER_PATH = installed_dir_path + "/vocoder/"
installed_DEFAULT_SYNTHESIZER_PATH = installed_dir_path + "/synthesizer/"
DEFAULT_URL = "https://github.com/blue-fish/Real-Time-Voice-Cloning/releases/download/v1.0/pretrained.zip"


def downloadModel(modelUrl=DEFAULT_URL):
    filepath = installed_dir_path + "/" + modelUrl.split('/')[-1]
    response = requests.get(modelUrl, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    # with urllib.request.urlopen(modelUrl) as f:
    with open(filepath, 'ab') as myfile:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            myfile.write(data)
        # myfile.write(f.read())
    progress_bar.close()

    return filepath
#I'm keeping the previous one because it works, but here is a more universal one
def downloadFile(destpath,fileurl):
    if not os.path.exists(destpath):
        os.mkdir(destpath)
    filepath=destpath+'/'+fileurl.split('/')[-1]
    response = requests.get(fileurl, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    # with urllib.request.urlopen(modelUrl) as f:
    with open(filepath, 'ab') as myfile:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            myfile.write(data)
        # myfile.write(f.read())
    progress_bar.close()

    return filepath




def extractModel(filepath):
    foldername = installed_dir_path + "/"  # +filepath.split('/')[-1].split('.')[0]
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(installed_dir_path)
    # shutil.rmtree(filepath)
    os.remove(filepath)
    return foldername


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            raise Exception('Directory not copied. Error: %s' % e)


# THIS WILL BE INITIALLY DESIGNED FOR DEFAULTS
# this needs to be reworked.
def getFullFilePath(rootfolder):
    finalfilepath = None
    for root, directories, filenames in os.walk(rootfolder):
        for filename in filenames:
            finalfilepath = str(os.path.join(root, filename))
    return finalfilepath


def installModels(folderpath, destpath=None):
    destdict = {"encoder": installed_DEFAULT_ENCODER_PATH, "vocoder": installed_DEFAULT_VOCODER_PATH,
                "synthesizer": installed_DEFAULT_SYNTHESIZER_PATH}
    for item in destdict:
        destdict[item] = getFullFilePath(destdict[item])
    return destdict


def installChecker(function, arglist=[]):
    # this is going to manage the variables the function gets called with
    global installed_path
    global installed_dir_path
    global installed_DEFAULT_ENCODER_PATH
    global installed_DEFAULT_VOCODER_PATH
    global installed_DEFAULT_SYNTHESIZER_PATH

    returnedvalue = None
    successfullycompleted = False
    while not successfullycompleted:
        try:
            if len(arglist) > 0:
                if len(arglist) == 2:
                    returnedvalue = function(arglist[0], arglist[1])
                else:
                    returnedvalue = function(arglist[0])
            else:
                returnedvalue = function()
            successfullycompleted = True
        except Exception as e:
            if "PERMISSION DENIED" in str(e).upper():
                print("Permission denied for downloading/installing to " + str(installed_dir_path) + "\n")
                installed_path = input("Please enter a new base path to download and install to >")
                installed_dir_path = os.path.dirname(installed_path)
                installed_DEFAULT_ENCODER_PATH = installed_dir_path + "/encoder/"
                installed_DEFAULT_VOCODER_PATH = installed_dir_path + "/vocoder/"
                installed_DEFAULT_SYNTHESIZER_PATH = installed_dir_path + "/synthesizer/"


                print("Trying again...")
    return returnedvalue


def defaultInstall():
    print("Downloading and installing default models, stand by...")
    zipfilepath = installChecker(downloadModel)
    extractedfolder = installChecker(extractModel, [zipfilepath])
    returned_dict = installChecker(installModels, [extractedfolder])
    return returned_dict
    # try:
    #    zipfilepath=downloadModel()
    #    extractedfolder=extractModel(zipfilepath)
    #    installModels(extractedfolder)
    #    return 1
    # except Exception as e:
    #    print(e)
    # return locationdict = {"encoder": encoderpath, "synthesizer": synthpath, "vocoder": vocoderpath}
