var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");
var audioPlayer = document.getElementById("audio_player");
var audio_file = document.getElementById("audio_file");
var uploadServer = document.getElementById("uploadServer");
// var userName = document.getElementById("userName");
var au = document.getElementById("audio_player");
var uploadResult = document.getElementById("uploadResult");
var textToSpeech = document.getElementById("tts");
var genAudio = document.getElementById("genAudio");
var genList = document.getElementById("genList");
var audioContext; //audio context to help us record
var wavContent; // storage file

