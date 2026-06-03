const API_HOST = window.location.hostname || "127.0.0.1";
const baseURL = `http://${API_HOST}:8000`;

export const LoginRequest = async (data) => {
  try {
    const response = await fetch(`${baseURL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error:", error);
    return { message: "Failed to connect to server" };
  }
};

export const RegisterRequest = async (data) => {
  try {
    const response = await fetch(`${baseURL}/auth/registration`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return { message: "Failed to register" };
  }
};

export const ForgotPasswordRequest = async (data) => {
  try {
    const response = await fetch(`${baseURL}/auth/forgot-password`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return { message: "Failed to send reset code" };
  }
};

export const ChangePasswordAfterVerification = async (data) => {
  try {
    const response = await fetch(`${baseURL}/auth/change-password-after-verification`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return { message: "Failed to change password" };
  }
};

export const ForgotPasswordRequest = async (data) => {
  try {
    const response = await fetch(`${baseURL}/auth/forgot-password`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    return result;

  } catch (error) {
    console.error("Error:", error);

    return {
      message: "Failed to send email",
    };
  }
};

export const ChangePasswordAfterVerification = async (data) => {
  try {
    const response = await fetch(`${baseURL}/auth/change-password-after-verification`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error:", error);
    return { message: "Failed to change password" };
  }
};


export const ChangePasswordRequest = async (data) => {
  try {
    const response = await fetch(`${baseURL}/auth/change-password`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return { message: "Failed to change password" };
  }
};

export const FetchCustomersRequest = async () => {
  try {
    const response = await fetch(`${baseURL}/auth/customers`);
    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return { message: "Error loading customers" };
  }
};

export const DeleteCustomerRequest = async (customerId) => {
  try {
    const response = await fetch(`${baseURL}/auth/delete-customer`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ customer_id: Number(customerId) }),
    });

    const result = await response.json();
    if (!response.ok && !result.message) {
      return { message: `Server error (${response.status})` };
    }
    return result;
  } catch (error) {
    console.error("Error:", error);
    return {
      message:
        "Cannot reach server. Open http://127.0.0.1:8000 and restart uvicorn.",
    };
  }
};

export const CreateCustomerRequest = async (packageId, customerName) => {
  try {
    const response = await fetch(`${baseURL}/auth/create-customer`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        package_id: packageId,
        customer_name: customerName,
      }),
    });

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return { message: "Error creating customer" };
  }
};
