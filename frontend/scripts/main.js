import { LoginRequest } from "./requests.js";

const loginButton = document.querySelector("#login-button");
const userInput = document.querySelector("#user-input");
const passwordInput = document.querySelector("#password-input");
const loginMessage = document.querySelector("#login-message");

loginButton.addEventListener("click", async (event) => {
  event.preventDefault();

  const user = userInput.value.trim();
  const pass = passwordInput.value;

  if (!user || !pass) {
    loginMessage.textContent = "Please enter username and password";
    return;
  }

  const result = await LoginRequest({ username: user, password: pass });

  if (!result.data) {
    loginMessage.textContent = result.message || "Login failed";
    return;
  }

  sessionStorage.setItem("customers", JSON.stringify(result.data.customers));
  sessionStorage.setItem("packages", JSON.stringify(result.data.packages));
  sessionStorage.setItem("username", result.username || user);
  window.location.href = "clients.html";
});
