import { RegisterRequest } from "./requests.js";

document.getElementById("registrationForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    await RegisterRequest(null, { username, email, password });
});
