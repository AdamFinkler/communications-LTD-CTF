

const baseURL = `${window.location.protocol}//${window.location.hostname}:8000`


export const LoginRequest = async (url, data) => {
  try {
    const response = await fetch(`${baseURL}/login`, {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json', 
      },
      body: JSON.stringify(data), 
    });

    if (!response.ok) {
      
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json(); 
    console.log('Success:', result);
  } catch (error) {
    console.error('Error:', error);
  }
};