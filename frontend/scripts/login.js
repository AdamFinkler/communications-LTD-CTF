import { LoginRequest } from "./requests.js";

document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    await LoginRequest(null, { username, password });
});
