console.log("✅ app.js carregado!");

// -------- Helpers --------
function getToken() {
  return localStorage.getItem("access_token") || "";
}

function getUser() {
  const raw = localStorage.getItem("user");
  try { return raw ? JSON.parse(raw) : null; } catch { return null; }
}

function authHeaders(extra = {}) {
  const h = { Accept: "application/json", ...extra };
  const token = getToken();
  if (token) h.Authorization = `Bearer ${token}`;
  return h;
}

function fmtMoney(n) {
  return Number(n).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

// -------- HTTP --------
async function apiGet(url) {
  const res = await fetch(url, { headers: authHeaders() });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.detail || `Erro ${res.status}`);
  return body;
}

async function apiPost(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: authHeaders({ "Content-Type": "application/json" }),
    body: JSON.stringify(data),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.detail || `Erro ${res.status}`);
  return body;
}

// -------- UI: Navbar --------
function setupNavbar() {
  const nameEl = document.getElementById("navUser");
  const btnAuth = document.getElementById("btnAuth");
  const btnLogout = document.getElementById("btnLogout");
  const user = getUser();
  const token = getToken();

  if (user && user.full_name && token) {
    const first = user.full_name.split(" ")[0];
    nameEl.textContent = `Olá, ${first} 👋`;
    nameEl.classList.remove("d-none");
    btnAuth.classList.add("d-none");
    btnLogout.classList.remove("d-none");
  } else {
    nameEl.classList.add("d-none");
    btnAuth.classList.remove("d-none");
    btnLogout.classList.add("d-none");
  }

  btnLogout?.addEventListener("click", () => {
    localStorage.clear();
    location.href = "/static/auth.html";
  });
}

// -------- Produtos --------
function renderTable(items = []) {
  const tbody = document.getElementById("tbody");
  tbody.innerHTML = "";
  items.forEach((p) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${p.id}</td>
      <td>${p.name}</td>
      <td>${p.category ?? "-"}</td>
      <td class="text-end">${fmtMoney(p.price ?? 0)}</td>`;
    tbody.appendChild(tr);
  });
}

async function loadList() {
  const params = new URLSearchParams();
  const q = document.getElementById("q").value.trim();
  const cat = document.getElementById("category").value.trim();
  const min = document.getElementById("min_price").value;
  const max = document.getElementById("max_price").value;
  const order = document.getElementById("order_by_price").checked;
  const limit = document.getElementById("limit").value || 20;
  const offset = document.getElementById("offset").value || 0;

  if (q) params.append("q", q);
  if (cat) params.append("category", cat);
  if (min !== "") params.append("min_price", min);
  if (max !== "") params.append("max_price", max);
  params.append("order_by_price", order);
  params.append("limit", limit);
  params.append("offset", offset);

  try {
    const data = await apiGet(`/products/?${params.toString()}`);
    renderTable(data);
  } catch (err) {
    alert("Erro: " + err.message);
  }
}

async function searchById() {
  const id = document.getElementById("by_id").value.trim();
  const out = document.getElementById("byIdOut");
  if (!id) return (out.textContent = "Informe um ID.");
  try {
    const data = await apiGet(`/products/${id}`);
    out.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    out.textContent = "Erro: " + err.message;
  }
}

async function createProduct(e) {
  e.preventDefault();
  const f = e.target;
  const payload = {
    name: f.name.value.trim(),
    category: f.category.value.trim(),
    price: Number(f.price.value),
  };
  const out = document.getElementById("createOut");
  try {
    const data = await apiPost("/products/", payload);
    out.textContent = "✅ Criado: " + JSON.stringify(data, null, 2);
    f.reset();
    loadList();
  } catch (err) {
    out.textContent = "❌ " + err.message;
  }
}

// -------- Init --------
document.addEventListener("DOMContentLoaded", () => {
  setupNavbar();
  document.getElementById("btnLoad")?.addEventListener("click", loadList);
  document.getElementById("btnSearchId")?.addEventListener("click", searchById);
  document.getElementById("formCreate")?.addEventListener("submit", createProduct);
  loadList();
});
