// Site du harness : apparitions au défilement, compteurs, pile de cartes. Aucune dépendance.
(function () {
  var calme = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Décalage entre les enfants d'un même groupe (stagger).
  document.querySelectorAll("[data-decale]").forEach(function (groupe) {
    var pas = parseFloat(groupe.getAttribute("data-decale")) || 0.08;
    Array.prototype.forEach.call(groupe.children, function (enfant, i) {
      enfant.style.setProperty("--d", (i * pas).toFixed(2) + "s");
    });
  });

  function compter(el) {
    var cible = parseInt(el.getAttribute("data-compte"), 10);
    if (calme || isNaN(cible)) { el.textContent = el.getAttribute("data-compte"); return; }
    var debut = null, duree = 1600;
    function pas(t) {
      if (debut === null) debut = t;
      var p = Math.min((t - debut) / duree, 1);
      var doux = 1 - Math.pow(1 - p, 4); // départ rapide, arrivée très douce
      el.textContent = Math.round(cible * doux);
      if (p < 1) requestAnimationFrame(pas);
    }
    requestAnimationFrame(pas);
  }

  function montrer(el) {
    el.classList.add("vu");
    if (el.hasAttribute("data-compte")) compter(el);
    if (el.classList.contains("frise")) el.style.setProperty("--remplissage", "1");
  }

  var cibles = document.querySelectorAll(".apparait, .masque, [data-compte], .frise");
  if (!("IntersectionObserver" in window)) {
    cibles.forEach(montrer);
  } else {
    var obs = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        if (e.isIntersecting) { montrer(e.target); obs.unobserve(e.target); } // une seule fois
      });
    }, { rootMargin: "0px 0px -80px 0px" });
    cibles.forEach(function (c) { obs.observe(c); });
  }

  // La navigation se resserre quand on défile.
  var nav = document.querySelector(".nav");
  if (nav) {
    var majNav = function () { nav.classList.toggle("serree", window.scrollY > 40); };
    window.addEventListener("scroll", majNav, { passive: true });
    majNav();
  }

  // Pile de cartes : la carte de devant part, les autres avancent d'un cran.
  document.querySelectorAll(".pile").forEach(function (pile) {
    var cartes = Array.prototype.slice.call(pile.querySelectorAll(".carte"));
    var n = cartes.length;
    cartes.forEach(function (c, i) { c.setAttribute("data-pos", String(Math.min(i, 3))); });
    if (calme || n < 2) return;
    var tete = 0, pause = false;
    pile.addEventListener("mouseenter", function () { pause = true; });
    pile.addEventListener("mouseleave", function () { pause = false; });
    setInterval(function () {
      if (pause || document.hidden) return;
      tete = (tete + 1) % n;
      cartes.forEach(function (c, i) {
        var pos = (i - tete + n) % n;
        c.setAttribute("data-pos", String(pos === n - 1 ? 3 : Math.min(pos, 2)));
        c.setAttribute("aria-hidden", pos === 0 ? "false" : "true");
      });
    }, 4500);
  });
})();
