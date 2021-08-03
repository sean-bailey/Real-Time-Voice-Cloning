"""
Provide an interface to enable:

1) Download and installation of pretrained models
2) Check if models are installed
3) If all systems go, have user input source sound for voice, text to be spoken, and it should create and return a sound
    -Do we need to save it as a wav, or can we just return the raw audio data to be processed?
    -Do we want to provide an auto-download-and-installation of the libri-speech dataset, and enable users to just select from those?
    -We could also provide the input of a folder to just select an audio from

When first loaded, this module should perform pre-flight checks, and report whether or not its going to fail out.
"""


def preFlightChecks():
    pass