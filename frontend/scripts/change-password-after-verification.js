import { ChangePasswordAfterVerification } from "./requests.js";

const changePasswordButton = document.querySelector("#change-password-button");
const usernameInput = document.querySelector("#change-username-input");
const newPasswordInput = document.querySelector("#change-new-password-input");
const message = document.querySelector("#change-password-message");

changePasswordButton.addEventListener("click", async (event) => {
  event.preventDefault();

  const payload = {
    username: usernameInput.value,
    new_password: newPasswordInput.value,
  };

  const result = await ChangePasswordAfterVerification(payload);
  message.textContent = result.message;
});
