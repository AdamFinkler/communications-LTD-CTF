import { ForgotPasswordRequest } from "./requests.js";

const forgotPasswordButton = document.querySelector("#send-email-button");
const emailInput = document.querySelector("#email-forgot-password");
const codeInput = document.querySelector("#verification-code");
const message = document.querySelector("#forgot-password-message");

let waitingForCode = false;

forgotPasswordButton.addEventListener(
  "click",
  async (event) => {
    event.preventDefault();

    const payload = {
      email: emailInput.value,
      code: waitingForCode
        ? codeInput.value
        : null,
    };

    const result = await ForgotPasswordRequest(payload);

    message.textContent =result.message;

    if (result.message ==="Password reset link sent to email")
     {
      waitingForCode = true;
      codeInput.style.display ="block";
      forgotPasswordButton.textContent = "Verify Code";
    }

    if (result.message === "Password reset successful")
       {
      window.location.replace("../pages/change-password-after-verification.html");
    }
  }
);