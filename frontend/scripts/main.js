import { LoginRequest } from "./requests.js";
import { arrayOfCustomers, arrayOfPackages } from "./global-data.js";

const loginForm = document.querySelector("form.login");
const loginButton = document.querySelector("#login-button");
const userInput = document.querySelector("#user-input");
const passwordInput = document.querySelector("#password-input");
const codeInput = document.querySelector("#code-input");
const loginError = document.querySelector("#login-error");

let waitingForCode = false;

// Listen on the form's submit so both the button click AND the Enter key
// run this handler — and preventDefault() stops the page from reloading,
// which would otherwise wipe the verification-code UI state.
loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const user = userInput.value;
  const pass = passwordInput.value;

  const result = await LoginRequest({
    username: user,
    password: pass,
    code: waitingForCode ? codeInput.value : null,
  });

  if (!result || !result.data) {
    loginError.textContent = result?.message || "Login failed. Please try again.";
    loginError.style.display = "block";

    if (result?.message === "A Verification Code was sent to youre Email") {
      waitingForCode = true;
      codeInput.style.display = "block";
      loginButton.textContent = "Verify Code";
    }
    return;
  }

  loginError.style.display = "none";

  arrayOfPackages.push(result.data.packages);
  arrayOfCustomers.push(result.data.customers);

  /* Using sessionStorage to store customer and package data,
      if not data will be lost */
  sessionStorage.setItem("customers", JSON.stringify(result.data.customers));
  sessionStorage.setItem("packages", JSON.stringify(result.data.packages));
  window.location.href = "clients.html";
});
