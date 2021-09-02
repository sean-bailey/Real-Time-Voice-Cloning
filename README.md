# Real-Time Voice Cloning Module: voiceCloner
## Background:
SV2TTS is a three-stage deep learning framework that allows to create a numerical representation of a voice from a few seconds of audio, and to use it to condition a text-to-speech model trained to generalize to new voices.

If you would like to learn more, I heavily encourage you to visit [Real-Time Voice Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning) by @CorentinJ, which I see as brilliant work.


This repository is a module based wrapper around [Real-Time Voice Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning). The general idea is to have a simple, importable, Pythonic API to perform programmatic voice cloning tasks with. I very highly recommend checking out the original work, as I cannot take any credit for the initial research and development.

I attempted to make this as simple to use as possible. In general, you will be able to install it, import it, and vocode a piece of text with any voice you can reference from any audio segment you can find -- including your own voice!
###Requirements:

Requirements for this module are identical to Real-Time Voice Cloning. Python3.8+.
* Install [PyTorch](https://pytorch.org/get-started/locally/) (>=1.0.1).
* Install [ffmpeg](https://ffmpeg.org/download.html#get-packages).

###Download Pretrained Models
Download the latest [here](https://github.com/CorentinJ/Real-Time-Voice-Cloning/wiki/Pretrained-models).

***Currently, you will need to download these models to get this module to function. This is a high priority work in progress to simplify this process.***

###Installation:

From the root of this repository, simply run:
```
pip3 install .
```

This will install voiceCloner into your Python location.

###Useage:
```
import rtvc
#when loaded, rtvc will run preFlightChecks, which will determine if your system is properly configured, has appropriate models installed, etc.
#It will fail if your system is not properly configured, or if you do not have appropriate encoder, vocoder and synthesizer models

rtvc.voiceclone(text="hello, world!",voiceactor="/path/to/spoken_voice.mp3")
```
The preFlightChecks will prompt you for the encoder, vocoder and synthesizer models if they
are not located within the default directory (rtvc/encoder, vocoder, and synthesizer, respectively).
Once you enter that information, however, the locations are saved in memory and are set as the defaults
for the module.

####voiceclone Class:
Inputs:
```
inputtext -- Required String, is the input text to be vocoded, default None
encoderpath -- Required encoder path, defaults to the DEFAULT_ENCODER_PATH
vocoderpath -- Required vocoder path, defaults to the DEFAULT_VOCODER_PATH
synthesizerpath -- Required synthesizer path, defaults to the DEFAULT_SYNTHESIZER_PATH
voiceactor -- Required String, is the path to the audio file to be referenced, Default None
savepath -- Optional String, is the path to the desired save location and type of vocoded audio output, Default None

```
Outputs:
```

generated_wav -- the generated vocoded wav as raw bytecode. Can be accessed directly, ideally by the soundfile module


```
