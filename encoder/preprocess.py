import os

from multiprocess.pool import ThreadPool
from encoder.params_data import *
from encoder.config import librispeech_datasets, anglophone_nationalites
from datetime import datetime
from encoder import audio
from pathlib import Path
from tqdm import tqdm
import numpy as np


class DatasetLog:
    """
    Registers metadata about the dataset in a text file.
    """
    def __init__(self, root, name):
        self.text_file = open(Path(root, "Log_%s.txt" % name.replace("/", "_")), "w")
        self.sample_data = dict()
        
        start_time = str(datetime.now().strftime("%A %d %B %Y at %H:%M"))
        self.write_line("Creating dataset %s on %s" % (name, start_time))
        self.write_line("-----")
        self._log_params()
        
    def _log_params(self):
        from encoder import params_data
        self.write_line("Parameter values:")
        for param_name in (p for p in dir(params_data) if not p.startswith("__")):
            value = getattr(params_data, param_name)
            self.write_line("\t%s: %s" % (param_name, value))
        self.write_line("-----")
    
    def write_line(self, line):
        self.text_file.write("%s\n" % line)
        
    def add_sample(self, **kwargs):
        for param_name, value in kwargs.items():
            if not param_name in self.sample_data:
                self.sample_data[param_name] = []
            self.sample_data[param_name].append(value)
            
    def finalize(self):
        self.write_line("Statistics:")
        for param_name, values in self.sample_data.items():
            self.write_line("\t%s:" % param_name)
            self.write_line("\t\tmin %.3f, max %.3f" % (np.min(values), np.max(values)))
            self.write_line("\t\tmean %.3f, median %.3f" % (np.mean(values), np.median(values)))
        self.write_line("-----")
        end_time = str(datetime.now().strftime("%A %d %B %Y at %H:%M"))
        self.write_line("Finished on %s" % end_time)
        self.text_file.close()
       
        
def _init_preprocess_dataset(dataset_name, datasets_root, out_dir) -> (Path, DatasetLog):
    dataset_root = datasets_root.joinpath(dataset_name)
    if not dataset_root.exists():
        print("Couldn\'t find %s, skipping this dataset." % dataset_root)
        return None, None
    return dataset_root, DatasetLog(out_dir, dataset_name)


def _preprocess_speaker_dirs(speaker_dirs, dataset_name, datasets_root, out_dir, extension,
                             skip_existing, logger):
    print("%s: Preprocessing data for %d lst." % (dataset_name, len(speaker_dirs)))
    
    # Function to preprocess utterances for one speaker
    def preprocess_speaker(speaker_dir: Path):
        # Give a name to the speaker that includes its dataset
        speaker_name = "_".join(speaker_dir.relative_to(datasets_root).parts)
        speaker_name = str(speaker_dir).split("/")[-1].split(".")[0]
        # print("speaker_name " +str(speaker_name))
        # Create an output directory with that name, as well as a txt file containing a 
        # reference to each source file.
        speaker_out_dir = out_dir.joinpath(speaker_name)
        # speaker_out_dir = out_dir
        # print("speaker_out_dir " + str(speaker_out_dir))
        speaker_out_dir.mkdir(exist_ok=True)
        sources_fpath = speaker_out_dir.joinpath("_sources.txt")
        # print("sources_fpath " + str(sources_fpath))
        # There's a possibility that the preprocessing was interrupted earlier, check if 
        # there already is a sources file.
        if sources_fpath.exists():
            try:
                with sources_fpath.open("r") as sources_file:
                    existing_fnames = {line.split(",")[0] for line in sources_file}
            except:
                existing_fnames = {}
        else:
            existing_fnames = {}
        
        # Gather all audio files for that speaker recursively
        sources_file = sources_fpath.open("a" if skip_existing else "w")
        # for in_fpath in speaker_dir.glob("**/*.%s" % extension):
        with open(speaker_dir, "r") as f_read:
            for line in f_read:
                in_fpath = line.split("\t")[1]
                elements = in_fpath.split("/")
                out_fname = "/".join(elements[elements.index("speech_data")+1:])
                # Check if the target output file already exists
                # out_fname = "_".join(in_fpath.relative_to(speaker_dir).parts)
                out_fname = out_fname.replace(".%s" % extension, ".npy")
                if skip_existing and out_fname in existing_fnames:
                    continue

                # Load and preprocess the waveform
                wav = audio.preprocess_wav(in_fpath)
                if len(wav) == 0:
                    continue

                # Create the mel spectrogram, discard those that are too short
                frames = audio.wav_to_mel_spectrogram(wav)
                if len(frames) < partials_n_frames:
                    continue

                out_fpath = speaker_out_dir.joinpath(out_fname)
                path_folder = "/".join(str(out_fpath).split("/")[:-1])
                os.makedirs(path_folder, exist_ok=True)
                np.save(out_fpath, frames)
                logger.add_sample(duration=len(wav) / sampling_rate)
                sources_file.write("%s,%s\n" % (out_fname, in_fpath))
        sources_file.close()
    
    # Process the utterances for each speaker
    with ThreadPool(8) as pool:
        list(tqdm(pool.imap(preprocess_speaker, speaker_dirs), dataset_name, len(speaker_dirs),
                  unit="speakers"))
    logger.finalize()
    print("Done preprocessing %s.\n" % dataset_name)


def preprocess_librispeech(datasets_root: Path, out_dir: Path, skip_existing=False):
    dataset_name = ""
    # Initialize the preprocessing
    dataset_root, logger = _init_preprocess_dataset(dataset_name, datasets_root, out_dir)
    if not dataset_root:
        return

    # Preprocess all speakers
    speaker_dirs = list(dataset_root.glob("*.lst"))
    print(speaker_dirs)
    _preprocess_speaker_dirs(speaker_dirs, dataset_name, datasets_root, out_dir, "wav",
                             skip_existing, logger)