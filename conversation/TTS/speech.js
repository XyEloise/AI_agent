// speech.js

// Speech Input - Using the Web Speech API's SpeechRecognition
export function startSpeechRecognition(questionInput) {
    // Check if the browser supports SpeechRecognition
    if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
        alert('Your browser does not support speech recognition.');
        return;
    }
  
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';  // Set the language to English
    recognition.continuous = false;  // Set to false for single recognition (stops after one speech)
  
    recognition.onstart = function() {
        console.log("Speech recognition started");
        alert("Voice recognition started, please speak now.");
    };
  
    recognition.onresult = function(event) {
        const userQuestion = event.results[0][0].transcript;
        console.log("Recognized speech: ", userQuestion);
        questionInput.value = userQuestion;  // Fill the recognized speech into the input box
    };
  
    recognition.onend = function() {
        console.log("Speech recognition ended");
    };
  
    recognition.onerror = function(event) {
        console.error("Speech recognition error", event.error);
        if (event.error === 'not-allowed') {
            alert("Permission to access the microphone is denied.");
        } else if (event.error === 'audio-capture') {
            alert("Microphone is not detected or cannot be accessed.");
        } else {
            alert("Speech recognition error. Please try again.");
        }
    };
  
    recognition.start();  // Start speech recognition
  }
  