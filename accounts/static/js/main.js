const messages = [
    "What can I do for you today?",
    "How can I make your day easier?",
    "What�s on your agenda today?",
    "How may I be of service to you?",
    "What are you curious about right now?",
    "Is there something I can solve for you?",
    "What would you like to explore together?",
    "What challenge can I help you tackle today?",
    "How can I assist in bringing your ideas to life?",
    "Got any questions for me today?"
    ];
    
    let index = 0;
    const textElement = document.getElementById("dynamicText");
    
    setInterval(() => {
    if (textElement) {
    textElement.textContent = messages[index];
    index = (index + 1) % messages.length;
    }
    }, 2000);
    function startVoiceInput() {
    if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.onresult = function(event) {
    document.querySelector('textarea').value = event.results[0][0].transcript;
    };
    recognition.start();
    } else {
    alert("Your browser does not support speech recognition.");
    }
    }
    // Function to send user input and handle the response
function sendUserInput() {
    const userInput = document.querySelector('#userInput').value;
    
    // Only send input if it's not empty
    if (userInput.trim() !== "") {
        // Display the user message in the chat (just for UI purposes)
        const chatMessages = document.getElementById('chatMessages');
        const userMessage = document.createElement('div');
        userMessage.classList.add('user-message');
        userMessage.textContent = userInput;
        chatMessages.appendChild(userMessage);
        
        // Clear input field
        document.querySelector('#userInput').value = '';

        // Send the user input to the backend for processing
        fetch(`/accounts/get_ai_response/?user_input=${encodeURIComponent(userInput)}`)
            .then(response => response.json())
            .then(data => {
                // Display the AI response in the chat
                const aiResponse = data.response;
                const aiMessage = document.createElement('div');
                aiMessage.classList.add('ai-message');
                aiMessage.textContent = aiResponse;
                chatMessages.appendChild(aiMessage);

                // Update mood based on response
                const mood = data.mood;
                updateMoodMeter(mood);
            })
            .catch(error => console.error('Error:', error));
    } else {
        alert("Please enter a message.");
    }
}

// Function to update the mood meter
function updateMoodMeter(mood) {
    const moodMeter = document.getElementById("moodMeter");
    const moodText = document.getElementById("moodText");

    // Update mood meter based on sentiment
    if (mood === 'positive') {
        moodMeter.className = "mood-positive";  // Set to green
        moodText.textContent = "Happy";
    } else if (mood === 'negative') {
        moodMeter.className = "mood-negative";  // Set to red
        moodText.textContent = "Sad";
    } else {
        moodMeter.className = "mood-neutral";  // Set to yellow
        moodText.textContent = "Neutral";
    }
}

// Add event listener for the "send" button
document.getElementById('sendMessage').addEventListener('click', sendUserInput);

// Optionally: Allow sending on "Enter" key press
document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // Prevents new line on Enter
        sendUserInput();
    }
});
function sendUserInput() {
    const userInput = document.querySelector('textarea').value;

    // Send the user input to the backend
    fetch('/get_ai_response/?user_input=' + encodeURIComponent(userInput))
        .then(response => response.json())
        .then(data => {
            const aiResponse = data.ai_response;
            const sentiment = data.sentiment;

            // Display the AI response
            document.getElementById("aiResponse").textContent = aiResponse;

            // Update the mood meter based on the sentiment
            updateMoodMeter(sentiment);
        })
        .catch(error => console.error('Error:', error));
}
function sendUserInput() {
    const userInput = document.querySelector('textarea').value;  // Get the user input from the textarea

    // Make an AJAX request to get the AI response
    fetch(`/get_ai_response/?user_input=${encodeURIComponent(userInput)}`)
        .then(response => response.json())
        .then(data => {
            const aiResponse = data.response;

            // Display the AI response in the chat area
            document.getElementById('aiResponse').textContent = aiResponse;

            // Determine the mood based on the AI response
            updateMood(aiResponse);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function updateMood(aiResponse) {
    const moodText = document.getElementById('moodText');
    const moodMeter = document.getElementById('moodMeter');

    // Simple logic to detect mood based on the AI response
    if (aiResponse.toLowerCase().includes("sad")) {
        moodText.textContent = 'Sad';
        moodMeter.className = 'mood-sad';  // Change to sad mood
    } else if (aiResponse.toLowerCase().includes("great") || aiResponse.toLowerCase().includes("good")) {
        moodText.textContent = 'Happy';
        moodMeter.className = 'mood-happy';  // Change to happy mood
    } else {
        moodText.textContent = 'Neutral';
        moodMeter.className = 'mood-neutral';  // Neutral mood
    }
}
