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
from rtvc.encoder.params_model import model_embedding_size as speaker_embedding_size
from rtvc.utils.argutils import print_args
from rtvc.utils.modelutils import check_model_paths
from rtvc.synthesizer.inference import Synthesizer
from rtvc.encoder import inference as encoder
from rtvc.vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
import argparse
import torch
import os
from audioread.exceptions import NoBackendError

USE_CPU=False
SUPPORT_MP3=True
DEFAULT_ENCODER_PATH="encoder/saved_models/pretrained.pt"
DEFAULT_VOCODER_PATH="vocoder/saved_models/pretrained/pretrained.pt"
DEFAULT_SYNTHESIZER_PATH="synthesizer/saved_models/pretrained/pretrained.pt"


#we just want to reutrn the audio -- not necessarily play it. No need to check if audio devices exist!
def preFlightChecks(download_models=False,using_cpu=False,mp3support=SUPPORT_MP3,encoderpath=None,synthpath=None,vocoderpath=None):
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    if encoderpath is None:
        #prompt user for encoder path, provide default for just entry
        encoderpath=input("Please enter the path to the encoder (hit enter to use default)> ") or DEFAULT_ENCODER_PATH
    if synthpath is None:
        synthpath=input("Please enter the path to the synthesizer model (hit enter to use default)> ") or DEFAULT_SYNTHESIZER_PATH
    if vocoderpath is None:
        vocoderpath=input("Please enter the path to the vocoder model (hit enter to use default)> ") or DEFAULT_VOCODER_PATH


    #we could always just specify defaults...
    #we don't want this to need any arguments, as it's supposed to run on start, which is at import. We won't have this info yet!!!
    #first we need to check for if the GPU is available...
    if mp3support:
        try:
            print("Debug: Loading Librosa...")
            #so this isn't working hardcoded. It cannot find the file. But I want this part of the module -- lets find out
            #how to locally reference things
            librosa.load(dir_path+"/samples/1320_00000.mp3")
        except NoBackendError:
            print("Librosa will be unable to open mp3 files if additional software is not installed.\n"
                  "Please install ffmpeg and restart the program, or continue with no MP3 support.")
            SUPPORT_MP3=False

    print("debug: checking if cuda is available")
    if torch.cuda.is_available():
        device_id = torch.cuda.current_device()
        gpu_properties = torch.cuda.get_device_properties(device_id)
        ## Print some environment information (for debugging purposes)
        #print("Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d with "
        #    "%.1fGb total memory.\n" %
        #    (torch.cuda.device_count(),
        #    device_id,
        #    gpu_properties.name,
        #    gpu_properties.major,
        #    gpu_properties.minor,
        #    gpu_properties.total_memory / 1e9))
    else:
        USE_CPU=True
    try:
        print("debug: checking model paths...")
        ## Remind the user to download pretrained models if needed
        #check_model_paths(encoder_path=encoderpath,
        #                  synthesizer_path=synthpath,
        #                  vocoder_path=vocoderpath)
        modelcheckdict=check_local_model_paths(encoderpath,synthpath,vocoderpath)
        #check if the models exist and are installed. If not, prompt the user if they would like auto installation TODO.
        #No. This should all be imported, which means it should only prompt if the input values are outside of default.
        #Otherwise, raise an error that ends the test saying to install the models and specify the paths before trying again
        if not (modelcheckdict['encoder'] and modelcheckdict['synthesizer'] and modelcheckdict['vocoder']):
            raise Exception("Could not locate models specified. Found Models: "+str(modelcheckdict))
            #that should hold for now until I master the auto installer. I'm putting too many features in the first run!
        ## Load the models one by one.
        encoderpath=Path(encoderpath)
        synthpath=Path(synthpath)
        vocoderpath=Path(vocoderpath)
        encoder.load_model(encoderpath)
        synthesizer = Synthesizer(synthpath)
        vocoder.load_model(vocoderpath)
        print("debug: running a test")
        ## Run a test
        # Forward an audio waveform of zeroes that lasts 1 second. Notice how we can get the encoder's
        # sampling rate, which may differ.
        # If you're unfamiliar with digital audio, know that it is encoded as an array of floats
        # (or sometimes integers, but mostly floats in this projects) ranging from -1 to 1.
        # The sampling rate is the number of values (samples) recorded per second, it is set to
        # 16000 for the encoder. Creating an array of length <sampling_rate> will always correspond
        # to an audio of 1 second.

        encoder.embed_utterance(np.zeros(encoder.sampling_rate))

        # Create a dummy embedding. You would normally use the embedding that encoder.embed_utterance
        # returns, but here we're going to make one ourselves just for the sake of showing that it's
        # possible.
        embed = np.random.rand(speaker_embedding_size)
        # Embeddings are L2-normalized (this isn't important here, but if you want to make your own
        # embeddings it will be).
        embed /= np.linalg.norm(embed)
        # The synthesizer can handle multiple inputs with batching. Let's create another embedding to
        # illustrate that
        embeds = [embed, np.zeros(speaker_embedding_size)]
        texts = ["test 1", "test 2"]
        #print("\tTesting the synthesizer... (loading the model will output a lot of text)")
        mels = synthesizer.synthesize_spectrograms(texts, embeds)

        # The vocoder synthesizes one waveform at a time, but it's more efficient for long ones. We
        # can concatenate the mel spectrograms to a single one.
        mel = np.concatenate(mels, axis=1)
        # The vocoder can take a callback function to display the generation. More on that later. For
        # now we'll simply hide it like this:
        no_action = lambda *args: None
        #print("\tTesting the vocoder...")
        # For the sake of making this test short, we'll pass a short target length. The target length
        # is the length of the wav segments that are processed in parallel. E.g. for audio sampled
        # at 16000 Hertz, a target length of 8000 means that the target audio will be cut in chunks of
        # 0.5 seconds which will all be generated together. The parameters here are absurdly short, and
        # that has a detrimental effect on the quality of the audio. The default parameters are
        # recommended in general.
        vocoder.infer_waveform(mel, target=200, overlap=50, progress_callback=no_action)

        return 1
    except Exception as e:
        raise Exception(str(e))


def check_local_model_paths(encpath,synthpath,vocpath):
    encfound=False
    synthfound=False
    vocfound=False
    if (os.path.exists(encpath)):
        encfound=True
    if os.path.exists(synthpath):
        synthfound=True
    if os.path.exists(vocpath):
        vocfound=True

    return {"encoder":encfound,"synthesizer":synthfound,"vocoder":vocfound}

#Okay. Now to have the class
#we need a forced text to vocode, an optional modelpath for encoder/vocoder/synthesizer, and a forced path to voice to model from.

class voiceclone:

    def __init__(self,inputtext=None,encoderpath=DEFAULT_ENCODER_PATH,vocoderpath=DEFAULT_VOCODER_PATH,synthesizerpath=DEFAULT_SYNTHESIZER_PATH,voiceactor=None,savepath=None):

        if inputtext is None:
            raise Exception("You must specify text to be vocoded into audio. ")
        if voiceactor is None:
            raise Exception("You must specify an input voice sample to synthesize from. ")

        modelcheckdict = check_local_model_paths(encoderpath, synthesizerpath, vocoderpath)
        if not (modelcheckdict['encoder'] and modelcheckdict['synthesizer'] and modelcheckdict['vocoder']):
            raise Exception("Could not locate models specified. Found Models: " + str(modelcheckdict))
        encoderpath=Path(encoderpath)
        synthesizerpath=Path(synthesizerpath)
        vocoderpath=Path(vocoderpath)
        encoder.load_model(encoderpath)
        synthesizer = Synthesizer(synthesizerpath)
        vocoder.load_model(vocoderpath)
        #finally we can actually give some meat to this thing...
        in_fpath = Path(voiceactor)#Path(input(voiceactor).replace("\"", "").replace("\'", ""))

        if in_fpath.suffix.lower() == ".mp3" and not SUPPORT_MP3:
            raise Exception("Your current installation does not support .mp3 files. Please specify another format and try again.")
        #preprocessed_wav = encoder.preprocess_wav(in_fpath)
        original_wav, sampling_rate = librosa.load(str(in_fpath))
        preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
        embed = encoder.embed_utterance(preprocessed_wav)
        # The synthesizer works in batch, so you need to put your data in a list or numpy array
        texts = [inputtext]
        embeds = [embed]
        # If you know what the attention layer alignments are, you can retrieve them here by
        # passing return_alignments=True
        specs = synthesizer.synthesize_spectrograms(texts, embeds)
        spec = specs[0]
        generated_wav = vocoder.infer_waveform(spec)
        generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

        # Trim excess silences to compensate for gaps in spectrograms (issue #53)
        generated_wav = encoder.preprocess_wav(generated_wav)
        if savepath is not None:
            sf.write(savepath,generated_wav.astype(np.float32),synthesizer.sample_rate)
        # Save it on the disk
        #filename = "demo_output_%02d.wav" % num_generated
        #print(generated_wav.dtype)
        #sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)
        #print("\nSaved output as %s\n\n" % filename)

preFlightChecks()