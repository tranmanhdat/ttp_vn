
python encoder_preprocess.py /root/src/data/speech_data/lst_process/lst/

python encoder_train.py pretrained /root/src/data/speech_data/lst_process/lst/SV2TTS/encoder/ --no_visdom

rename my_run.pt in encoder/saved_models to pretrained.pt hoặc sửa my_run thành pretrained

python synthesizer_preprocess_audio.py ../dataset/custom_data/test -o /root/src/Text2Speech/dataset/custom_data/speech_data --no_alignments

python synthesizer_train.py my_run ../dataset/custom_data/speech_data/SV2TTS/synthesizer

python vocoder_preprocess.py dont_need --model_dir synthesizer/saved_models/my_run/ -i ../dataset/custom_data/speech_data/SV2TTS/synthesizer/ -o ../dataset/custom_data/speech_data/SV2TTS/vocoder

