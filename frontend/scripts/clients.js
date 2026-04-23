import { DeleteCustomerRequest } from "./requests.js";

if (!sessionStorage.getItem("customers")) window.location.href = "login.html"; // Redirect if no data in sessionStorage

const customers = JSON.parse(sessionStorage.getItem("customers"));
const packageMap = Object.fromEntries(
  JSON.parse(sessionStorage.getItem("packages")).map((p) => [p[0], p])
);

const container = document.querySelector(".clients-container");

const handleDelete = async (customerName) => {
  const result = await DeleteCustomerRequest(customerName);

  if (result.message.includes("successfully")) {
    const updatedCustomers = customers.filter(([_, name]) => name !== customerName);
    sessionStorage.setItem("customers", JSON.stringify(updatedCustomers));

    document.querySelectorAll(".client-row").forEach(row => {
      if (row.querySelector(`[data-customer="${customerName}"]`)) {
        row.remove();
      }
    });
  } else {
    alert("Error: " + result.message);
  }
};

customers.forEach(([packageId, customerName]) => {
  const pkg = packageMap[packageId];
  container.insertAdjacentHTML(
    "beforeend",
    `<span class="client-row" data-customer="${customerName}">
      <p>${customerName}</p>
      <p>${pkg ? pkg[1] : "Unknown"}</p>
      <p>${pkg ? `$${Number(pkg[4]).toFixed(2)}` : "-"}</p>
      <button class="delete-btn" data-customer="${customerName}">Delete</button>
    </span>`
  );
});

document.querySelectorAll(".delete-btn").forEach(btn => {
  btn.addEventListener("click", (e) => {
    const customerName = e.target.getAttribute("data-customer");
    if (confirm(`Are you sure you want to delete ${customerName}?`)) {
      handleDelete(customerName);
    }
  });
});
