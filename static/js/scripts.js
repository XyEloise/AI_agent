document.addEventListener('DOMContentLoaded', function() {  
    const userForm = document.getElementById('userForm');
    const questionInput = document.getElementById('questionInput');
    const chatContainer = document.getElementById('chatContainer');
    const audioButton = document.getElementById('audioButton');  
    const recordingIndicator = document.getElementById('recordingIndicator');  
    const closeRecording = document.getElementById('closeRecording'); 

    // Speech recognition
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';  
    recognition.continuous = true;  
    
    // When the audio button is clicked, start speech recognition
    audioButton.addEventListener('click', function() {
        recognition.start();  
        recordingIndicator.style.display = 'flex';  
    });

    // Speech recognition result
    recognition.onresult = function(event) {
        const userQuestion = event.results[0][0].transcript;
        questionInput.value = userQuestion;  // Fill the recognized speech into the input box
    };

    // Speech recognition ended
    recognition.onend = function() {
        console.log("Speech recognition ended");
        recordingIndicator.style.display = 'none';  // Hide recording indicator
    };

    // Speech recognition error
    recognition.onerror = function(event) {
        console.error("Speech recognition error", event.error);
        recordingIndicator.style.display = 'none';  // Hide recording indicator
    };

    // Stop recording button
    closeRecording.addEventListener('click', function() {
        recognition.stop();  // Stop speech recognition
        recordingIndicator.style.display = 'none';  // Hide recording indicator
    });

    // Submit form
    userForm.addEventListener('submit', function(e) {
        e.preventDefault();  // Prevent default form submission behavior
        console.log("Form submitted");
        
        const question = questionInput.value.trim();  
        const session_id = "session_" + Date.now();  
        
        // Check if the question is empty
        if (!question) {
            alert('Please enter a question!');
            return;
        }

        // Add the user's message
        const userMessageDiv = document.createElement('div');
        userMessageDiv.classList.add('message', 'user-message');
        const now = new Date();
        const timeString = now.getHours() + ':' + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes();
        userMessageDiv.innerHTML = `${question}<div class="timestamp">${timeString}</div>`;
        chatContainer.appendChild(userMessageDiv);

        // Clear the input box
        questionInput.value = '';
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // Send request to backend
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question, session_id: session_id })
        })
        .then(response => response.json())
        .then(data => {
            // Create AI response container
            const aiMessageDiv = document.createElement('div');
            aiMessageDiv.classList.add('message', 'ai-message');
            const aiTime = new Date();
            const aiTimeString = aiTime.getHours() + ':' + (aiTime.getMinutes() < 10 ? '0' : '') + aiTime.getMinutes();
            const answerId = `currentAnswer_${session_id}`;
            aiMessageDiv.innerHTML = `
                <span id="${answerId}"></span>
                <div class="timestamp">${aiTimeString}</div>
            `;
            chatContainer.appendChild(aiMessageDiv);

            // 添加语音输出按钮
            const speakButton = document.createElement('button');
            speakButton.classList.add('speak-button');
            speakButton.textContent = '🔊 Speak';
            aiMessageDiv.appendChild(speakButton);

            // Get reference to the answer element
            const currentAnswerElement = document.getElementById(answerId);

            let fullAnswer = '';
            let isCompleted = false;
            let retryCount = 0;
            const maxRetries = 3;
            const receivedChunks = [];

            let hasSpoken = false; // 标志变量，确保语音只播放一次

            // Polling for streaming data
            const interval = setInterval(function() {
                if (isCompleted) return;
                
                fetch(`/get_answer?session_id=${session_id}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(responseData => {
                        retryCount = 0;
                        
                        if (responseData.answer === "END") {
                            isCompleted = true;
                            clearInterval(interval);
                            fullAnswer = receivedChunks.join('');
                            currentAnswerElement.innerText = fullAnswer;
                            
                            // 确保语音只播放一次
                            if (!hasSpoken) {
                                speakAnswer(fullAnswer);  // 语音输出
                                hasSpoken = true;
                            }
                            return;
                        }
                        
                        if (responseData.answer) {
                            receivedChunks.push(responseData.answer);
                            fullAnswer += responseData.answer;
                            currentAnswerElement.innerText = fullAnswer;
                            chatContainer.scrollTop = chatContainer.scrollHeight;
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        retryCount++;
                        if (retryCount >= maxRetries) {
                            clearInterval(interval);
                            alert("Error getting response. Please try again.");
                        }
                    });
            }, 200);  // Set polling interval

            // 语音输出：点击按钮播放语音
            speakButton.addEventListener('click', function() {
                speakAnswer(fullAnswer);  // 语音输出
                hasSpoken = true;  // 设置标志，确保只播放一次
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Request failed, please try again.");
        });
    });

    // Speech Output
    function speakAnswer(answer) {
        const utterance = new SpeechSynthesisUtterance(answer);
        utterance.lang = 'en-US';  
        speechSynthesis.speak(utterance);
        console.log("Speaking: ", answer);
    }
});
