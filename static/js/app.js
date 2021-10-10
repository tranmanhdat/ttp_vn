//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;
var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording
var AudioContext = window.AudioContext || window.webkitAudioContext;


recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);
uploadServer.addEventListener("click", startUpload);
genAudio.addEventListener("click", startGenAudio);


audio_file.onchange = function () {
    var files = this.files;
    var file = URL.createObjectURL(files[0]);
    wavContent = files[0];
    audioPlayer.src = file;
    // audio_player.play();
    uploadServer.disabled = false;
};
// userName.onchange = function () {
//     uploadServer.disabled = userName.value.length <= 0;
//     // console.log(uploadServer.disabled);
// };

textToSpeech.onchange = function () {
    genAudio.disabled = textToSpeech.value.length <= 0;
    // console.log(textToSpeech.value.length);
    // console.log(genAudio.disabled);
};

function startRecording() {
    console.log("recordButton clicked");
    var constraints = {audio: true, video: false};
    recordButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false;
    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        audioContext = new AudioContext();
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);
        rec = new Recorder(input, {numChannels: 1});
        rec.record();
        console.log("Recording started");
    }).catch(function (err) {
        //enable the record button if getUserMedia() fails
        recordButton.disabled = false;
        stopButton.disabled = true;
        pauseButton.disabled = true
    });
}

function pauseRecording() {
    console.log("pauseButton clicked rec.recording=", rec.recording);
    if (rec.recording) {
        rec.stop();
        pauseButton.innerHTML = "Resume";
    } else {
        rec.record();
        pauseButton.innerHTML = "Pause";

    }
}

function stopRecording() {
    console.log("stopButton clicked");
    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;
    pauseButton.innerHTML = "Pause";
    rec.stop();
    gumStream.getAudioTracks()[0].stop();
    rec.exportWAV(createDownloadLink);
}


function createDownloadLink(blob) {

    var url = URL.createObjectURL(blob);
    // var au = document.createElement('audio');

    //name of .wav file to use during upload and download (without extendion)
    new Date().toISOString();
//add controls to the <audio> element
    au.controls = true;
    au.src = url;
    // au.play();
    wavContent = blob;
    //upload link
    // var upload = document.createElement('a');
    // upload.href = "#";
    // upload.innerHTML = "Upload";
}

function startUpload() {
    var xhr = new XMLHttpRequest();
    xhr.onload = function (e) {
        if (this.readyState === 4) {
            uploadResult.textContent = e.target.responseText;
        }
    };
    var fd = new FormData();
    fd.append("audio_data", wavContent);
    // fd.append("user_name", userName.value);
    xhr.open("POST", "/upload_audio", true);
    xhr.send(fd);
}

function startGenAudio() {
    // audioPlayerGen.src = "/gen_audio";
    var xhr = new XMLHttpRequest();
    xhr.onload = function (e) {
        if (this.readyState === 4 && this.status === 200) {
            var content = this.response.toString();
            var fileName = JSON.parse(content).name;
            var au = document.createElement('audio');
            au.controls = true;
            au.controlsList="nodownload";
            au.src = '/get_audio?file_name=' + fileName;
            var downloadButton = document.createElement('a');
            downloadButton.href = '/get_audio?file_name=' + fileName;
            // downloadButton.target = '';
            // downloadButton.download = fileName;
            var t = document.createTextNode("Download");
            downloadButton.appendChild(t);
            var li = document.createElement('li');
            li.appendChild(document.createTextNode(fileName + ".wav : " + textToSpeech.value));
            li.appendChild(au);
            li.appendChild(downloadButton);
            genList.appendChild(li);
        }
    };
    var fd = new FormData();
    fd.append("tts", textToSpeech.value);
    xhr.open("POST", "/gen_audio", true);
    xhr.send(fd);

}