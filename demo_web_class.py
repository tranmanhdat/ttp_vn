from encoder.params_model import model_embedding_size as speaker_embedding_size
from utils.modelutils import check_model_paths
from utils.argutils import print_args
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
import argparse
import torch
import os


class TextToSpeech:
    def __init__(self, encoder_path, synthesizer_path, vocoder_path):
        check_model_paths(encoder_path=encoder_path,
                          synthesizer_path=synthesizer_path,
                          vocoder_path=vocoder_path)

        ## Load the models one by one.
        print("Preparing the encoder, the synthesizer and the vocoder...")
        encoder.load_model(encoder_path)
        self.synthesizer = Synthesizer(synthesizer_path)
        vocoder.load_model(vocoder_path)
        ## Run a test
        # print("Testing your configuration with small inputs.")
        # # Forward an audio waveform of zeroes that lasts 1 second. Notice how we can get the encoder's
        # # sampling rate, which may differ.
        # # If you're unfamiliar with digital audio, know that it is encoded as an array of floats
        # # (or sometimes integers, but mostly floats in this projects) ranging from -1 to 1.
        # # The sampling rate is the number of values (samples) recorded per second, it is set to
        # # 16000 for the encoder. Creating an array of length <sampling_rate> will always correspond
        # # to an audio of 1 second.
        # print("\tTesting the encoder...")
        # encoder.embed_utterance(np.zeros(encoder.sampling_rate))
        #
        # # Create a dummy embedding. You would normally use the embedding that encoder.embed_utterance
        # # returns, but here we're going to make one ourselves just for the sake of showing that it's
        # # possible.
        # embed = np.random.rand(speaker_embedding_size)
        # # Embeddings are L2-normalized (this isn't important here, but if you want to make your own
        # # embeddings it will be).
        # embed /= np.linalg.norm(embed)
        # # The synthesizer can handle multiple inputs with batching. Let's create another embedding to
        # # illustrate that
        # embeds = [embed, np.zeros(speaker_embedding_size)]
        # texts = ["mẫu 1", "mẫu 2"]
        # print("\tTesting the synthesizer... (loading the model will output a lot of text)")
        # mels = self.synthesizer.synthesize_spectrograms(texts, embeds)
        #
        # # The vocoder synthesizes one waveform at a time, but it's more efficient for long ones. We
        # # can concatenate the mel spectrograms to a single one.
        # mel = np.concatenate(mels, axis=1)
        # # The vocoder can take a callback function to display the generation. More on that later. For
        # # now we'll simply hide it like this:
        # print("\tTesting the vocoder...")
        # # For the sake of making this test short, we'll pass a short target length. The target length
        # # is the length of the wav segments that are processed in parallel. E.g. for audio sampled
        # # at 16000 Hertz, a target length of 8000 means that the target audio will be cut in chunks of
        # # 0.5 seconds which will all be generated together. The parameters here are absurdly short, and
        # # that has a detrimental effect on the quality of the audio. The default parameters are
        # # recommended in general.
        # vocoder.infer_waveform(mel, target=200, overlap=50)
        # print("All test passed! You can now synthesize speech.\n\n")
        self.embed = None

    def take_sample(self, audio_file):
        # Get the reference audio filepath
        in_fpath = Path(audio_file)
        ## Computing the embedding
        # First, we load the wav using the function that the speaker encoder provides. This is
        # important: there is preprocessing that must be applied.

        # The following two methods are equivalent:
        # - Directly load from the filepath:
        # preprocessed_wav = encoder.preprocess_wav(in_fpath)
        # - If the wav is already loaded:
        original_wav, sampling_rate = librosa.load(str(in_fpath))
        preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
        print("Loaded file succesfully")
        # Then we derive the embedding. There are many functions and parameters that the
        # speaker encoder interfaces. These are mostly for in-depth research. You will typically
        # only use this function (with its default parameters):
        self.embed = encoder.embed_utterance(preprocessed_wav)
        # print(self.embed)
        # print(sum(self.embed))
        print("Created the embedding")

    def gen_audio(self, text, audio_path):
        ## Generating the spectrogram

        # The synthesizer works in batch, so you need to put your data in a list or numpy array
        texts, padding = self.split_text(text)
        print(texts)
        embeds = [self.embed.copy()] * len(texts)
        # print(text)
        # If you know what the attention layer alignments are, you can retrieve them here by
        # passing return_alignments=True
        specs = self.synthesizer.synthesize_spectrograms(texts, embeds)
        print("Created the mel spectrogram")
        ## Generating the waveform
        print("Synthesizing the waveform:")
        # spec = specs[0]
        list_generate_wav = []
        i = 0
        for spec in specs:
            # Synthesizing the waveform is fairly straightforward. Remember that the longer the
            # spectrogram, the more time-efficient the vocoder.
            generated_wav = vocoder.infer_waveform(spec)

            ## Post-generation
            # There's a bug with sounddevice that makes the audio cut one second earlier, so we
            # pad it.
            generated_wav = np.pad(generated_wav, (0, self.synthesizer.sample_rate), mode="constant")

            # Trim excess silences to compensate for gaps in spectrograms (issue #53)
            generated_wav = encoder.preprocess_wav(generated_wav)
            generated_wav = np.pad(generated_wav, (0, int(self.synthesizer.sample_rate*padding[i])), mode="constant")
            list_generate_wav.append(generated_wav)
            # path_audio = "/root/src/Text2Speech/tts_vn/static/audio_download/" + str(i)+".wav"
            i = i +  1
            # sf.write(path_audio, generated_wav.astype(np.float32), self.synthesizer.sample_rate)
        generated_wav = np.concatenate(list_generate_wav)
        # Save it on the disk
        print(generated_wav.dtype)
        sf.write(audio_path, generated_wav.astype(np.float32), self.synthesizer.sample_rate)
        print("\nSaved output as %s\n\n" % audio_path)

    def split_text(self, text):
        """
        split text to small pieces to generate
        Args:
            text: need to divide

        Returns:
            texts: list of small pieces text
            padding: denote padding type (, or . or something else)
        """
        # temp_text = text.replace(",", ".").replace(";", ".").replace(":", ".").replace("!", ".").replace("?", ".")
        padding_time = {",":0.25,".":0.5,":":0.5,";":0.5}
        elements = " ".join(text.split(" ")).split(" ")
        list_text = []
        tmp_text = []
        len_tmp_text = 0
        padding = []
        for element in elements:
            if element in padding_time:
                if len_tmp_text>0:
                    list_text.append(" ".join(tmp_text))
                    tmp_text = []
                    len_tmp_text = 0
                padding.append(padding_time[element])
            else:
                tmp_text.append(element)
                len_tmp_text = len_tmp_text + 1
                if len_tmp_text==15:
                    list_text.append(" ".join(tmp_text))
                    padding.append(0)
                    tmp_text = []
                    len_tmp_text = 0
        if 0 < len_tmp_text < 15:
            list_text.append(" ".join(tmp_text))
            padding.append(0)
        return list_text, padding

def init():
    ## Info & args
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-e", "--enc_model_fpath", type=Path,
                        default="encoder/saved_models/pretrained.pt",
                        help="Path to a saved encoder")
    parser.add_argument("-s", "--syn_model_fpath", type=Path,
                        default="synthesizer/saved_models/pretrained/pretrained.pt",
                        help="Path to a saved synthesizer")
    parser.add_argument("-v", "--voc_model_fpath", type=Path,
                        default="vocoder/saved_models/pretrained/pretrained.pt",
                        help="Path to a saved vocoder")
    parser.add_argument("--cpu", action="store_true", help= \
        "If True, processing is done on CPU, even when a GPU is available.")
    args = parser.parse_args()
    print_args(args, parser)

    if args.cpu:
        # Hide GPUs from Pytorch to force CPU processing
        os.environ["CUDA_VISIBLE_DEVICES"] = ""

    print("Running a test of your configuration...\n")

    if torch.cuda.is_available():
        device_id = torch.cuda.current_device()
        gpu_properties = torch.cuda.get_device_properties(device_id)
        ## Print some environment information (for debugging purposes)
        print("Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d with "
              "%.1fGb total memory.\n" %
              (torch.cuda.device_count(),
               device_id,
               gpu_properties.name,
               gpu_properties.major,
               gpu_properties.minor,
               gpu_properties.total_memory / 1e9))
    else:
        print("Using CPU for inference.\n")
    return args