(function () {
  const racine = document.documentElement;
  const systemeSombre = matchMedia("(prefers-color-scheme: dark)");
  const boutonTheme = document.querySelector(".nav-theme");

  function sombreActif() {
    return racine.dataset.theme ? racine.dataset.theme === "dark" : systemeSombre.matches;
  }

  function afficherTheme() {
    const sombre = sombreActif();
    boutonTheme.dataset.mode = sombre ? "sombre" : "clair";
    boutonTheme.setAttribute("aria-label", sombre ? "Passer en mode clair" : "Passer en mode sombre");
  }

  boutonTheme.hidden = false;
  boutonTheme.addEventListener("click", () => {
    const choix = sombreActif() ? "light" : "dark";
    racine.dataset.theme = choix;
    try { localStorage.setItem("harness-theme", choix); } catch {}
    afficherTheme();
  });
  systemeSombre.addEventListener("change", afficherTheme);
  afficherTheme();

  const menu = document.querySelector(".nav-menu");
  const liens = document.querySelector(".nav-liens");
  const mobile = matchMedia("(max-width: 47.99rem)");

  function ouvrirMenu(ouvert) {
    liens.hidden = mobile.matches && !ouvert;
    menu.setAttribute("aria-expanded", String(!liens.hidden && mobile.matches));
  }

  menu.hidden = false;
  ouvrirMenu(false);
  mobile.addEventListener("change", () => ouvrirMenu(false));
  menu.addEventListener("click", () => ouvrirMenu(liens.hidden));
  menu.closest("nav").addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu.getAttribute("aria-expanded") === "true") {
      ouvrirMenu(false);
      menu.focus();
    }
  });

  if (!matchMedia("(prefers-reduced-motion: no-preference)").matches || !("IntersectionObserver" in window)) return;

  document.querySelectorAll("[data-decale]").forEach((groupe) => {
    const pas = Number(groupe.dataset.decale);
    Array.from(groupe.children).forEach((enfant, index) => {
      enfant.style.setProperty("--d", Math.min(index * pas, .25) + "s");
    });
  });

  const cibles = document.querySelectorAll(".apparait, .masque");
  const observateur = new IntersectionObserver((entrees) => {
    entrees.forEach((entree) => {
      if (!entree.isIntersecting) return;
      entree.target.classList.add("vu");
      observateur.unobserve(entree.target);
    });
  }, { rootMargin: "0px 0px -32px 0px" });

  cibles.forEach((cible) => observateur.observe(cible));
})();
