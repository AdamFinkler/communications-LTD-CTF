import {
  DeleteCustomerRequest,
  CreateCustomerRequest,
  FetchCustomersRequest,
} from "./requests.js";

if (!sessionStorage.getItem("packages")) {
  window.location.href = "login.html";
}

const container = document.querySelector(".clients-container");
const addCustomerBtn = document.getElementById("add-customer-btn");
const modal = document.getElementById("customer-modal");
const cancelBtn = document.getElementById("cancel-btn");
const modalOverlay = document.querySelector(".modal-overlay");
const customerForm = document.getElementById("customer-form");
const customerNameInput = document.getElementById("customer-name");
const packageSelect = document.getElementById("package-select");
const newCustomerBanner = document.getElementById("new-customer-banner");

const packages = JSON.parse(sessionStorage.getItem("packages"));
const packageMap = Object.fromEntries(packages.map((p) => [p[0], p]));

let customers = [];

const showBanner = (text, isError = false) => {
  newCustomerBanner.hidden = false;
  newCustomerBanner.textContent = text;
  newCustomerBanner.style.background = isError ? "#ffebee" : "";
  newCustomerBanner.style.borderColor = isError ? "#f44336" : "";
};

const reloadCustomersTable = (customerList) => {
  container.querySelectorAll(".client-row:not(:first-child)").forEach((row) => row.remove());
  customers = customerList;
  sessionStorage.setItem("customers", JSON.stringify(customers));
  customers.forEach(([customerId, packageId, customerName]) => {
    renderCustomerRow(customerId, packageId, customerName);
  });
};

const renderCustomerRow = (customerId, packageId, customerName) => {
  const pkg = packageMap[packageId];
  const row = document.createElement("span");
  row.className = "client-row";
  row.dataset.customerId = String(customerId);

  const idEl = document.createElement("p");
  idEl.className = "customer-id";
  idEl.textContent = `#${customerId}`;

  const nameEl = document.createElement("p");
  // Stored XSS vulnerability: customer names are inserted as HTML without escaping.
  nameEl.innerHTML = customerName;

  const packageEl = document.createElement("p");
  packageEl.textContent = pkg ? pkg[1] : "Unknown";

  const priceEl = document.createElement("p");
  priceEl.textContent = pkg ? `$${Number(pkg[4]).toFixed(2)}` : "-";

  const deleteBtn = document.createElement("button");
  deleteBtn.className = "delete-btn";
  deleteBtn.type = "button";
  deleteBtn.textContent = "Delete";
  deleteBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    const id = Number(row.dataset.customerId);
    if (confirm(`Delete customer #${id}?`)) {
      handleDelete(id);
    }
  });

  row.append(idEl, nameEl, packageEl, priceEl, deleteBtn);
  container.appendChild(row);
};

const renderPackageDropdown = () => {
  packages.forEach(([packageId, packageName, downloadSpeed, uploadSpeed]) => {
    const option = document.createElement("option");
    option.value = packageId;
    option.textContent = `${packageName} - ${downloadSpeed}/${uploadSpeed}`;
    packageSelect.appendChild(option);
  });
};

const loadCustomersFromServer = async () => {
  const result = await FetchCustomersRequest();
  if (result.customers) {
    reloadCustomersTable(result.customers);
    return true;
  }
  showBanner(
    "Could not load customers. Use http://127.0.0.1:8000 and restart the server.",
    true
  );
  return false;
};

const handleDelete = async (customerId) => {
  if (!customerId) {
    showBanner("Invalid customer ID", true);
    return;
  }

  const result = await DeleteCustomerRequest(customerId);

  if (result.message && result.message.includes("successfully") && result.customers) {
    reloadCustomersTable(result.customers);
    showBanner(`Customer #${customerId} deleted successfully`);
    return;
  }

  showBanner(`Delete failed: ${result.message || "unknown error"}`, true);
  await loadCustomersFromServer();
};

const handleCreateCustomer = async (e) => {
  e.preventDefault();

  const customerName = customerNameInput.value.trim();
  const packageId = parseInt(packageSelect.value, 10);

  if (!customerName || !packageId) {
    showBanner("Please fill in all fields", true);
    return;
  }

  const result = await CreateCustomerRequest(packageId, customerName);

  if (result.message && result.message.includes("successfully") && result.customers) {
    const previousCount = customers.length;
    reloadCustomersTable(result.customers);
    const addedCount = result.customers.length - previousCount;

    if (addedCount > 1) {
      showBanner(`SQLi demo: ${addedCount} customers added`);
    } else {
      const last = result.customers[result.customers.length - 1];
      showBanner(`New customer added: #${last[0]} ${last[2]}`);
    }

    customerForm.reset();
    modal.classList.remove("active");
  } else {
    showBanner(`Create failed: ${result.message || "unknown error"}`, true);
  }
};

renderPackageDropdown();
loadCustomersFromServer();

addCustomerBtn.addEventListener("click", () => modal.classList.add("active"));
cancelBtn.addEventListener("click", () => modal.classList.remove("active"));
modalOverlay.addEventListener("click", () => modal.classList.remove("active"));
customerForm.addEventListener("submit", handleCreateCustomer);
