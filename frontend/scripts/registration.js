import { RegisterRequest } from "./requests.js";

const registrationForm = document.querySelector("#registration-form");
const message = document.querySelector("#registration-message");

registrationForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    username: document.querySelector("#username-input").value.trim(),
    email: document.querySelector("#email-input").value.trim(),
    password: document.querySelector("#password-input").value,
  };

  const result = await RegisterRequest(payload);
  message.textContent = result.message;

  if (result.message === "User registered successfully") {
    setTimeout(() => {
      window.location.href = "login.html";
    }, 1200);
  }
});
