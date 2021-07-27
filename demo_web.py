import os
import shutil
from datetime import datetime

from demo_web_class import init, TextToSpeech
from flask import Flask, render_template, request, flash, redirect, session, send_from_directory, jsonify
from deploy_support.process_text import text_preprocess

app = Flask(__name__)
app.secret_key = "abc_xyz"

app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/audio_upload/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['DOWNLOAD_FOLDER'] = os.getcwd() + '/static/audio_download/'
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if request.method == 'POST':
        files = request.files.getlist('audio_data')
        save_name_upload = datetime.now().strftime('%y_%m_%d_%H_%M_%S') + ".wav"
        if files.count == 0:
            flash('No file selected for uploading')
            return redirect(request.url)
        else:
            path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], save_name_upload)
            files[0].save(path_to_file)
            print("Saved", path_to_file)
            tts.take_sample(path_to_file)
            return "Upload {} Done!".format(save_name_upload)


@app.route('/gen_audio', methods=['POST'])
def gen_audio():
    if request.method == 'POST':
        text = request.form['tts']
        print("Processing: {}".format(text))
        text = text_preprocess(text)
        print("Done: {}".format(text))
        save_name = datetime.now().strftime('%y%m%d%H%M%S')
        save_name_download = save_name + ".wav"
        path_text = os.path.join(app.config['DOWNLOAD_FOLDER'], save_name + ".txt")
        with open(path_text, "w+") as f_write:
            f_write.write(text)
        path_to_save = os.path.join(app.config['DOWNLOAD_FOLDER'], save_name_download)
        tts.gen_audio(text, path_to_save)
        return jsonify({"name":save_name})

@app.route('/get_audio')
def get_audio():
    file_name = request.args.get('file_name')
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], file_name+".wav", as_attachment=True,
                                   mimetype="audio/wav")

if __name__ == '__main__':
    args = init()
    tts = TextToSpeech(encoder_path=args.enc_model_fpath,
                       synthesizer_path=args.syn_model_fpath,
                       vocoder_path=args.voc_model_fpath)
    app.run(debug=True, port=8081, host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
