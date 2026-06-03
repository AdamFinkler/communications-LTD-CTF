import { ForgotPasswordRequest } from "./requests.js";

const forgotPasswordButton = document.querySelector("#send-email-button");
const emailInput = document.querySelector("#email-forgot-password");
const codeInput = document.querySelector("#verification-code");
const message = document.querySelector("#forgot-password-message");

let waitingForCode = false;

forgotPasswordButton.addEventListener("click", async (event) => {
  event.preventDefault();

  const payload = {
    email: emailInput.value.trim(),
    code: waitingForCode ? codeInput.value.trim() : null,
  };

  const result = await ForgotPasswordRequest(payload);
  message.textContent = result.hint
    ? `${result.message}. ${result.hint}`
    : result.message;

  if (result.message === "Password reset code sent to email") {
    waitingForCode = true;
    codeInput.style.display = "block";
    forgotPasswordButton.textContent = "Verify Code";
  }

  if (result.verified) {
    sessionStorage.setItem("resetEmail", payload.email);
    window.location.href = "change-password-after-verification.html";
  }
});
