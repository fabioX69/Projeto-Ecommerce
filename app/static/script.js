(function(){
  const token = localStorage.getItem("access_token");
  const userLabel = document.getElementById("userLabel");
  const btnLogout = document.getElementById("btnLogout");
  const btnLogin = document.getElementById("btnLogin");

  if (token) {
    if (userLabel) userLabel.textContent = "Logado";
    if (btnLogout) btnLogout.classList.remove("d-none");
    if (btnLogin) btnLogin.classList.add("d-none");
    if (btnLogout) btnLogout.onclick = () => { localStorage.removeItem("access_token"); location.href="/"; };
  } else {
    if (btnLogout) btnLogout.classList.add("d-none");
    if (btnLogin) btnLogin.classList.remove("d-none");
  }
})();
