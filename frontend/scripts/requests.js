const baseURL = `${window.location.protocol}//${window.location.hostname}:8000`;

export const LoginRequest = async (data) => {
  try {
    const response = await fetch(`${baseURL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log("results are: ", result);
    return result.data;
  } catch (error) {
    console.error("Error:", error);
  }
};
