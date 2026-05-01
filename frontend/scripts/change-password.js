import { ChangePasswordRequest } from "./requests.js";

const changePasswordButton = document.querySelector("#change-password-button");
const usernameInput = document.querySelector("#change-username-input");
const currentPasswordInput = document.querySelector("#change-current-password-input");
const newPasswordInput = document.querySelector("#change-new-password-input");
const message = document.querySelector("#change-password-message");

changePasswordButton.addEventListener("click", async (event) => {
  event.preventDefault();

  const payload = {
    username: usernameInput.value,
    current_password: currentPasswordInput.value,
    new_password: newPasswordInput.value,
  };

  const result = await ChangePasswordRequest(payload);
  message.textContent = result.message;
});
