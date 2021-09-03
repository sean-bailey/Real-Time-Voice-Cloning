# Real-Time Voice Cloning Module: voiceCloner

## Background:

SV2TTS is a three-stage deep learning framework that allows to create a numerical representation of a voice from a few
seconds of audio, and to use it to condition a text-to-speech model trained to generalize to new voices.

If you would like to learn more, I heavily encourage you to
visit [Real-Time Voice Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning) by @CorentinJ, which I see as
brilliant work.

This repository is a module based wrapper
around [Real-Time Voice Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning). The general idea is to have a
simple, importable, Pythonic API to perform programmatic voice cloning tasks with. I very highly recommend checking out
the original work, as I cannot take any credit for the initial research and development.

I attempted to make this as simple to use as possible. In general, you will be able to install it, import it, and vocode
a piece of text with any voice you can reference from any audio segment you can find -- including your own voice!

### Requirements:

Requirements for this module are identical to Real-Time Voice Cloning. Python3.8+.

* Install [PyTorch](https://pytorch.org/get-started/locally/) (>=1.0.1).
* Install [ffmpeg](https://ffmpeg.org/download.html#get-packages).

### Download Pretrained Models

~~Download the latest [here](https://github.com/CorentinJ/Real-Time-Voice-Cloning/wiki/Pretrained-models).~~

~~***Currently, you will need to download these models to get this module to function. This is a high priority work in
progress to simplify this process.***~~

The current iteration of this code will automatically attempt to download and install the pretrained models into the
library's location for you. If it is unsuccessful due to permissions issues (say you installed this library
with `sudo pip3 install .`), then it will prompt you for the appropriate install location.

### Installation:

From the root of this repository, simply run:

```
pip3 install .
```

This will install voiceCloner into your Python location.

### Useage:

```
import rtvc

#it is highly recommended to run rtvc.preFlightChecks(), determine if your system is properly configured, attempt to download and install default models, has appropriate models installed, etc.
#preFlightChecks() has the following options:
#download_models -- Boolean, defaults True, tells function whether or not to automatically download and install default models
#using_cpu -- Boolean, defaults False, flag of function to configure CPU or GPU (or to try with GPU at all)
#mp3support -- Boolean, defaults True (but checks anyways), flag to check for / confirm mp3 support
#encoderpath -- String, defaults to the DEFAULT_ENCODER_PATH, set to your encoder model path
#vocoderpath -- String, defaults to the DEFAULT_VOCODER_PATH, set to your vocoder model path
#synthpath -- String, defaults to the DEFAULT_SYNTHESIZER_PATH, set to your synthesizer path

rtvc.preFlightChecks()

#you will know if all systems check out if you see
#"Done."

rtvc.voiceclone(text="hello, world!",voiceactor="/path/to/spoken_voice.mp3")
```

Once preFlightChecks gets a valid encoder/vocoder/synthesizer model location, then for this session it will save it as
the default locations, providing easy reference.

#### voiceclone Class:

Inputs:

```
inputtext -- Required String, is the input text to be vocoded, default None
encoderpath -- Required encoder path, defaults to the DEFAULT_ENCODER_PATH if not specified (with original default of None)
vocoderpath -- Required vocoder path, defaults to the DEFAULT_VOCODER_PATH if not specified (with original default of None)
synthesizerpath -- Required synthesizer path, defaults to the DEFAULT_SYNTHESIZER_PATH if not specified (with original default of None)
voiceactor -- Required String, is the path to the audio file to be referenced, Default None
savepath -- Optional String, is the path to the desired save location and type of vocoded audio output, Default None

```

Outputs:

```

generated_wav -- the generated vocoded wav as raw bytecode. Can be accessed directly, ideally by the soundfile module


```

##CONTRIBUTING:
If you'd like to contribute to this repo, please see the instructions in `CONTRIBUTING.md`.