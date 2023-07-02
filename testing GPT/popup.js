// Function to send a message
function sendMessage() {
  const input = document.querySelector('.message-input');
  const message = input.value.trim();

  if (message !== '') {
    // Replace 'YOUR_API_KEY' with your actual API key
    const apiKey = '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';

    // Prepare the request data
    const requestData = {
      message: message,
    };

    // Send the message to your API and handle the response
    fetch('https://api.openai.com/v3/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiKey // Include the API key in the Authorization header
      },
      body: JSON.stringify(requestData)
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response from the API
        const responseMessage = data.response;
        // Do something with the response message, e.g., display it in the chat interface

        // Clear the input field
        input.value = '';
      })
      .catch(error => {
        // Handle any errors that occurred during the API request
        console.error('Error:', error);
      });
  }
}

// Event listener for the send button
const sendButton = document.querySelector('.send-button');
sendButton.addEventListener('click', sendMessage);

// Event listener for the enter key in the input field
const messageInput = document.querySelector('.message-input');
messageInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    sendMessage();
  }
});
