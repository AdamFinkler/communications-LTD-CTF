import { LoginRequest } from "./requests.js";
import { arrayOfCustomers, arrayOfPackages } from "./global-data.js";

const loginButton = document.querySelector("#login-button");
const userInput = document.querySelector("#user-input");
const passwordInput = document.querySelector("#password-input");

loginButton.addEventListener("click", async (event) => {
  event.preventDefault();

  const user = userInput.value;
  const pass = passwordInput.value;

  const data = await LoginRequest({ username: user, password: pass });

  arrayOfPackages.push(data.packages);
  arrayOfCustomers.push(data.customers);

});


