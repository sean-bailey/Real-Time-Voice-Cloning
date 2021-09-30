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
import uuid
import requests
from tqdm import tqdm


DEFAULT_URL = "https://github.com/blue-fish/Real-Time-Voice-Cloning/releases/download/v1.0/pretrained.zip"


def downloadModel(argdict):
    tempdirpath=argdict['tempdirpath']
    if "modelUrl" in argdict.keys():
        modelUrl=argdict['modelUrl']
    else:
        modelUrl=DEFAULT_URL
    if not os.path.exists(tempdirpath):
        os.mkdir(tempdirpath)
    filepath=os.path.abspath(tempdirpath)+modelUrl.split('/')[-1]
    #filepath = installed_dir_path + "/" + modelUrl.split('/')[-1]
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


def extractModel(argdict):
    filepath=argdict['filepath']
    tempdir=argdict['tempdirpath']
    encoder=argdict['encoder']
    vocoder=argdict['vocoder']
    synthesizer=argdict['synthesizer']
    #actually, at this point we know that one of them does not exist. We don't know which ones.
    #check to see if each exists. IF not, then create a directory for each and copy the extracted data into it.
    tempdict={"encoder":encoder,"vocoder":vocoder,"synthesizer":synthesizer}
    outputdict=tempdict
    copydict={"encoder":False,"vocoder":False,"synthesizer":False}
    for key in tempdict.keys():
        #for some unknown reason we are failing here. it's just hanging. why?
        tempfullpath=os.path.abspath(tempdict[key])
        #I don't understand -- it's stuck in an infinite loop
        if os.path.exists(tempfullpath):
            if os.path.isfile(tempfullpath):
                continue
            else:
                copydict[key]=True #we do need to copy the file
                #turns out that shutil.copytree copies the outer directory too

                if os.path.exists(tempfullpath+"/"+key):
                    shutil.rmtree(tempfullpath+"/"+key)
                #    os.mkdir(tempfullpath+"/"+key)
                #I wonder -- it loops here. Is this "resetting" the item in the loop?
                #easy way to find out...
                outputdict[key]=tempfullpath+"/"+key
        else:
            print("This dir doesn't exist. making it...")
            os.mkdir(tempfullpath)
            copydict[key] = True  # we do need to copy the file
            if os.path.exists(tempfullpath + "/" + key):
                shutil.rmtree(tempfullpath + "/" + key)
            #os.mkdir(tempfullpath + "/" + key)
            outputdict[key] = tempfullpath + "/" + key
    #so we need to actually get clever. We need to see if we need the encoder, vocoder and synthesizer.
    #idea: extractall to temporary directory, then use the copy function to copy appropriately, and then delete the temp
    #dir.
    #foldername = installed_dir_path + "/"  # +filepath.split('/')[-1].split('.')[0]
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(tempdir)
    for key in copydict.keys():
        if copydict[key]:
            copy(tempdir+"/"+key,tempdict[key])

    shutil.rmtree(tempdir)
    # shutil.rmtree(filepath)

    os.remove(filepath)
    return outputdict


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


def verifyModels(argdict):
    destdict = {"encoder": argdict["encoder"], "vocoder": argdict['vocoder'],
                "synthesizer": argdict['synthesizer']}
    for item in destdict:
        destdict[item] = getFullFilePath(destdict[item])
    return destdict

#ok so global vables here are goofing everything up. That's not how I want to do things.


def installChecker(function, argdict):
    # this is going to manage the variables the function gets called with

    returnedvalue = None
    successfullycompleted = False
    while not successfullycompleted:
        try:
            returnedvalue=function(argdict)
            successfullycompleted = True
        except Exception as e:
            testing=input(str(e))
            if "PERMISSION DENIED" in str(e).upper():
                print("Permission denied for downloading/installing to " + str(os.path.dirname(os.path.abspath(argdict['encoder']))) + "\n")
                installed_path = input("Please enter a new base path to download and install to >")
                argdict['encoder']=argdict['vocoder']=argdict['synthesizer']=installed_path
                argdict['tempdirpath']=os.path.dirname(os.path.abspath(installed_path))+"/"+argdict['tempdirpath'].split('/')[-1]
                print("Trying again...")
    return returnedvalue,argdict


def defaultInstall(encoderpath,vocoderpath,synthpath):

    #so it all starts here.
    #let's have it check for encoderpath, vocoderpath and synthpath.
    #we know if we are here that the files do not exist.
    # Create the encoder/vocoder/synthesizer directory
    #as necessary. have a flag for which models need installing. Extract the models from the zip file to a temporary
    #folder, and then copy only the appropriate models to the appropriate directory.
    #return the model paths.
    argdict={}
    tempdirpath=os.path.dirname(os.path.abspath(encoderpath))+"/"+str(uuid.uuid4())
    print("Downloading and installing default models, stand by...")
    argdict["tempdirpath"]=tempdirpath

    #use a dictionary instead of a list of arguments.

    argdict['encoder']=encoderpath
    argdict['vocoder']=vocoderpath
    argdict['synthesizer']=synthpath
    print("debug: getting zipfilepath")
    zipfilepath, argdict = installChecker(downloadModel, argdict)
    argdict['filepath'] = zipfilepath
    print("debug: getting extracted folders")
    extractedfolders,argdict = installChecker(extractModel, argdict)
    argdict['encoder']=extractedfolders['encoder']
    argdict['vocoder']=extractedfolders['vocoder']
    argdict['synthesizer']=extractedfolders['synthesizer']
    print("debug: verifying install")
    returned_dict,argdict = installChecker(verifyModels, argdict)
    return returned_dict

