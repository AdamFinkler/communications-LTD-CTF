const customers = JSON.parse(sessionStorage.getItem("customers") ?? "[]");
const packages = JSON.parse(sessionStorage.getItem("packages") ?? "[]");

const packageMap = Object.fromEntries(packages.map((p) => [p[0], p]));

function renderClients() {
  const container = document.querySelector(".clients-container");

  customers.forEach(([packageId, customerName]) => {
    const pkg = packageMap[packageId];
    const packageName = pkg ? pkg[1] : "Unknown";
    const monthlyPrice = pkg ? `$${Number(pkg[4]).toFixed(2)}` : "-";

    const row = document.createElement("span");
    row.className = "client-row";
    row.innerHTML = `
      <p>${customerName}</p>
      <p>${packageName}</p>
      <p>${monthlyPrice}</p>
    `;
    container.appendChild(row);
  });
}

renderClients();
