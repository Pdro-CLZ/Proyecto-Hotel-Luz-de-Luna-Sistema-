function filterTable() {
  const name = document.getElementById("filterName").value.toLowerCase();
  const type = document.getElementById("filterType").value;
  const rows = document.querySelectorAll("#inventoryTable tr");

  rows.forEach(row => {
    const nameCell = row.cells[1].textContent.toLowerCase();
    const typeCell = row.cells[3].textContent.toLowerCase();
    let show = true;

    if (name && !nameCell.includes(name)) show = false;
    if (type && typeCell !== type) show = false;

    row.style.display = show ? "" : "none";
  });
}

function clearFilters() {
  document.getElementById("filterName").value = "";
  document.getElementById("filterType").value = "";
  const rows = document.querySelectorAll("#inventoryTable tr");
  rows.forEach(row => row.style.display = "");
}

function toggleStatus(button) {
  const row = button.closest("tr");
  const statusCell = row.cells[5];
  if (statusCell.textContent.includes("Activo")) {
    statusCell.innerHTML = '<span class="badge bg-secondary">Inactivo</span>';
    button.textContent = "Activar";
  } else {
    statusCell.innerHTML = '<span class="badge bg-success">Activo</span>';
    button.textContent = "Inactivar";
  }
}


