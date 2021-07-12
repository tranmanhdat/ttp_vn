suppose:
- data in /path_data/data/speech_data so in docker it should be in /root/src/data/speech_data
- lst files should be in /path_data/data/lst
- clone repo to /path_data/data : git clone https://github.com/tranmanhdat/tts_vn
- disk stored data should have at least 200gb empty

1. create docker images:
docker run --runtime=nvidia -itd --ipc=host -p 8081:8081 --volume /path_data/:/root/src --name rtvc
tranmanhdat/rtvc:base

2. train model:
docker exec -it rtvc bash
cd /root/src/data/tts_vn
python encoder_preprocess.py /root/src/data/lst/
python encoder_train.py pretrained /root/src/data/lst/SV2TTS/encoder/ --no_visdom

python synthesizer_preprocess_audio.py /root/src/data/lst -o /root/src/data/lst --no_alignments -n 8
python synthesizer_preprocess_embeds.py /root/src/data/lst/SV2TTS/synthesizer/
python synthesizer_train.py pretrained /root/src/data/lst/SV2TTS/synthesizer/

python vocoder_preprocess.py /root/src/data/lst -i /root/src/data/lst/SV2TTS/synthesizer/ -o /root/src/data/lst/SV2TTS/vocoder
python vocoder_train.py pretrained /root/src/data/lst

3. test:
python demo_web.py