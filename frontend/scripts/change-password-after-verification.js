import { ChangePasswordAfterVerification } from "./requests.js";

const changePasswordButton = document.querySelector("#change-password-button");
const emailInput = document.querySelector("#change-email-input");
const newPasswordInput = document.querySelector("#change-new-password-input");
const message = document.querySelector("#change-password-message");

const resetEmail = sessionStorage.getItem("resetEmail");
if (!resetEmail) {
  message.textContent = "Complete forgot-password verification first";
} else {
  emailInput.value = resetEmail;
}

changePasswordButton.addEventListener("click", async (event) => {
  event.preventDefault();

  const payload = {
    email: emailInput.value.trim(),
    new_password: newPasswordInput.value,
  };

  const result = await ChangePasswordAfterVerification(payload);
  message.textContent = result.message;

  if (result.message === "Password changed successfully") {
    sessionStorage.removeItem("resetEmail");
    setTimeout(() => {
      window.location.href = "login.html";
    }, 1200);
  }
});
