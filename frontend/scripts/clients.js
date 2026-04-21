if (!sessionStorage.getItem("customers")) window.location.href = "login.html"; // Redirect if no data in sessionStorage

const customers = JSON.parse(sessionStorage.getItem("customers"));
const packageMap = Object.fromEntries(
  JSON.parse(sessionStorage.getItem("packages")).map((p) => [p[0], p])
);

const container = document.querySelector(".clients-container");

customers.forEach(([packageId, customerName]) => {
  const pkg = packageMap[packageId];
  container.insertAdjacentHTML(
    "beforeend",
    `<span class="client-row">
      <p>${customerName}</p>
      <p>${pkg ? pkg[1] : "Unknown"}</p>
      <p>${pkg ? `$${Number(pkg[4]).toFixed(2)}` : "-"}</p>
    </span>`
  );
});
