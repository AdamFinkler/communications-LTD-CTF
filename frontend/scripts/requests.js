

const baseURL = "http://127.0.0.1:8000"

const LoginRequest = async (url, data) => {
  try {
    const response = await fetch(url, {
      method: 'POST', // Specify the method
      headers: {
        'Content-Type': 'application/json', // Indicate the content type
      },
      body: JSON.stringify(data), // Convert the JavaScript object to a JSON string
    });

    if (!response.ok) {
      // Handle non-successful responses (e.g., 404, 500)
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json(); // Parse the JSON response
    console.log('Success:', result);
  } catch (error) {
    console.error('Error:', error);
  }
};