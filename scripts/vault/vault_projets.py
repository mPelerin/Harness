#!/usr/bin/env python3
"""Outil du vault « Projets ».

  modele                 régénère _Modèles/, _Méthode/, l'accueil et les vues Bases
  nouveau NOM [--depot propriétaire/dépôt]   crée NOM/ depuis la structure (le code va dans NOM/code)
  completer NOM          ajoute à un projet existant les notes apparues dans la structure, sans rien écraser
  recap                  régénère le récap de chaque projet et le tableau de bord, depuis GitHub
  verifier [DOSSIER]     liens cassés, propriétés manquantes, noms en double, texte en double

La structure d'un projet vit dans structure.py, seul endroit à modifier.
"""
import argparse, collections, datetime as dt, json, os, re, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from structure import SECTIONS, MODELES_NOTES  # noqa: E402

def lire_conf(cle, conf=None):
    """Valeur de harness.conf (instance), sans exécuter le fichier. Vide si absente."""
    if conf is None:
        conf = Path(os.environ.get("HARNESS_CONF", Path.home() / ".config/harness/harness.conf"))
    if conf.exists():
        for ligne in conf.read_text(encoding="utf-8").splitlines():
            if ligne.startswith(cle + "="):
                return ligne.split("=", 1)[1].strip()
    return ""


def racine_vault():
    valeur = (
        os.environ.get("VAULT_PROJETS")
        or lire_conf("RACINE_PROJETS", Path.home() / ".config/harness-local/harness.conf")
        or lire_conf("RACINE_PROJETS")
        or "."
    )
    return Path(valeur).expanduser().resolve()


VAULT = racine_vault()
PRENOM = lire_conf("PRENOM") or "l'utilisateur"
HUMAIN = PRENOM.lower() if PRENOM != "l'utilisateur" else "humain"
DEBUT, FIN = "<!-- debut:auto -->", "<!-- fin:auto -->"
PROPRIETES = ["projet", "type", "statut", "agent", "resume", "haut", "precedent", "suivant"]
STATUTS_TICKET = {
    "a-faire": "À faire", "en-cours": "En cours", "en-revue": "En revue",
    "en-preprod": "En préprod", "en-ligne": "En ligne", "ferme": "Fermé sans suite",
}


# ---------- écriture ----------

HORODATAGE = re.compile(r"Généré le \d{4}-\d{2}-\d{2} \d{2}:\d{2}")


def ecrire(chemin: Path, texte: str, ecraser=True) -> bool:
    """Écrit seulement si le contenu change, horodatage mis à part : évite de réveiller la synchro pour rien."""
    if chemin.exists():
        ancien = chemin.read_text(encoding="utf-8")
        if not ecraser or HORODATAGE.sub("", ancien) == HORODATAGE.sub("", texte):
            return False
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(texte, encoding="utf-8")
    return True


def lien(titre):
    return f'"[[{titre}]]"' if titre else '""'


def frontmatter(d: dict) -> str:
    lignes = ["---"]
    for k, v in d.items():
        lignes.append(f"{k}: {v}" if v not in (None, "") else f"{k}:")
    return "\n".join(lignes + ["---", ""])


# ---------- structure d'un projet ----------

def parcours(nom):
    """Ordre de lecture du projet : sommaire de section, puis ses notes, puis section suivante."""
    ordre = []
    for s in SECTIONS:
        sommaire = f"{nom} - {s['dossier']}"
        ordre.append((s, sommaire, None))
        for n in s["notes"]:
            ordre.append((s, f"{nom} - {n[0]}", n))
    return ordre


def generer_projet(racine: Path, nom: str, depot="", ecraser=False):
    ordre = parcours(nom)
    ecrits = 0
    for i, (s, titre, note) in enumerate(ordre):
        prec = ordre[i - 1][1] if i > 0 else nom
        suiv = ordre[i + 1][1] if i + 1 < len(ordre) else ""
        dossier = racine / s["dossier"]
        sommaire = f"{nom} - {s['dossier']}"
        if note is None:
            if "profil_phase" in s:
                profil = dossier / "agent.md"
                if not profil.exists():
                    modele = VAULT / "_Modèles" / "Projet" / s["dossier"] / "agent.md"
                    texte_profil = modele.read_text(encoding="utf-8") if modele.is_file() else s["profil_phase"]
                    ecrits += ecrire(profil, texte_profil, ecraser=False)
            fm = {"projet": lien(nom), "type": "sommaire", "statut": "valide", "agent": "",
                  "resume": f'"{s["sujet"]}"', "haut": lien(nom), "precedent": lien(prec), "suivant": lien(suiv)}
            corps = [f"# {s['dossier'][3:]}", "", s["sujet"], ""]
            if s["notes"]:
                corps += ["## Dans l'ordre de lecture", ""]
                corps += [f"{k}. [[{nom} - {n[0]}]] : {n[3]}" for k, n in enumerate(s["notes"], 1)]
            if s["dossier"] == "05 Tickets":
                corps += ["", f"Les tickets et leur statut, à jour depuis GitHub : [[{nom} - GitHub]]."]
            if s["dossier"] == "09 Journal":
                corps += ["## Comptes rendus", "", "<!-- Une note par séance, modèle « Compte rendu ». -->"]
            texte = frontmatter(fm) + "\n".join(corps) + "\n"
        else:
            t, typ, agent, resume, corps = note
            fm = {"projet": lien(nom), "type": typ, "statut": "a-faire", "agent": HUMAIN if agent == "HUMAIN" else agent,
                  "resume": f'"{resume}"', "haut": lien(sommaire), "precedent": lien(prec), "suivant": lien(suiv)}
            texte = frontmatter(fm) + f"# {t}\n\n> {resume}\n\n" + corps
        chemin = dossier / f"{titre}.md"
        if chemin.exists() and not ecraser and note is None:
            # un sommaire est généré : on le réécrit, en gardant son bloc automatique (liste des tickets)
            ancien = chemin.read_text(encoding="utf-8")
            bloc = re.search(re.escape(DEBUT) + r".*?" + re.escape(FIN), ancien, re.S)
            if bloc and DEBUT in texte:
                texte = re.sub(re.escape(DEBUT) + r".*?" + re.escape(FIN), lambda _: bloc.group(0), texte, flags=re.S)
            ecrits += ecrire(chemin, texte)
        elif chemin.exists() and not ecraser:
            ancien = chemin.read_text(encoding="utf-8")
            neuf = ancien
            for cle in ("haut", "precedent", "suivant"):
                neuf = re.sub(rf"^{cle}:.*$", f"{cle}: {fm[cle]}", neuf, count=1, flags=re.M)
            ecrits += ecrire(chemin, neuf)
        else:
            ecrits += ecrire(chemin, texte, ecraser)
    ecrits += ecrire(racine / f"{nom}.md", note_projet(nom, depot), ecraser)
    ecrits += ecrire(racine / f"{nom} - GitHub.md", note_github(nom), ecraser)
    return ecrits


def note_github(nom):
    fm = {"projet": lien(nom), "type": "suivi", "statut": "valide",
          "resume": '"Généré depuis GitHub : avancement, tickets, branches et mises en ligne."', "haut": lien(nom)}
    return frontmatter(fm) + "\n".join([
        "# GitHub", "", DEBUT, "Généré par `vault_projets.py recap` depuis le dépôt (propriété `depot` de la note projet).", FIN, ""])


def note_projet(nom, depot):
    fm = {"type": "projet", "statut": "actif", "phase": "discovery", "depot": depot,
          "prod": "", "preprod": "", "resume": '""',
          "suivant": lien(f"{nom} - {SECTIONS[0]['dossier']}")}
    sommaire = [f"- [[{nom} - {s['dossier']}]] : {s['sujet']}" for s in SECTIONS]
    return frontmatter(fm) + "\n".join([
        f"# {nom}", "",
        "> [!summary] En une phrase", "> À écrire : le problème, pour qui, et ce que le projet change.", "",
        "## Suivi", "", f"Avancement, tickets et branches : [[{nom} - GitHub]].", "",
        "## Sommaire", "", *sommaire, "",
    ])


# ---------- modèle, méthode, accueil ----------

CONVENTIONS = """---
type: methode
statut: valide
resume: "Nommage, propriétés, liens et accès des agents dans le vault Projets."
---

# Conventions du vault Projets

> Ce fichier est généré par `vault_projets.py modele`. Modifier la structure du classeur dans `scripts/vault/structure.py` du moteur.

## Arborescence

```
00 Accueil.md                 point d'entrée de tout le vault
00 Tableau de bord.md         généré : tous les projets, leur avancement
_Méthode/                     ces conventions et les vues Bases
_Modèles/Projet/              le dossier projet type (projet fictif « PROJET »)
_Modèles/Notes/               notes isolées : ticket, décision, entretien, atelier, compte rendu
_À trier/                     temporaire : documents d'avant le vault, à réintégrer
<Nom>/<Nom>.md                note projet : en une phrase, phase, sommaire
<Nom>/<Nom> - GitHub.md       généré : avancement, tickets, branches, mises en ligne
<Nom>/01 Discovery/ … 09 Journal/
<Nom>/                        le dépôt Git du projet, poussé sur GitHub : notes, AGENTS.md, .github/
<Nom>/code/                   l'appli (package.json, src/…) ; toutes ses commandes se lancent ici
```

Le vault est le dossier `RACINE_PROJETS` de `harness.conf`. Ce qui est exclu de GitHub par le `.gitignore` est aussi exclu de la synchro : bibliothèques, builds, base locale, secrets, `.git`. La note `<Nom> - GitHub` est générée et jamais versionnée. Un agent travaille un ticket dans un worktree, pour que le dossier synchronisé reste sur `preprod`.

## Nommage

- Toute note d'un projet commence par le nom du projet : `Mon-appli - PRD`, `Mon-appli - 03 Design`. Un lien `[[Mon-appli - PRD]]` n'est donc jamais ambigu.
- Les dossiers de section sont numérotés `01` à `09` dans l'ordre de vie du projet.
- Un ticket : `<Nom> - T<numéro> <titre court>`, par exemple `Mon-appli - T06 Réserver un cadeau`. Le numéro est celui de l'issue GitHub.
- Un compte rendu : `<Nom> - CR AAAA-MM-JJ <sujet>`.
- Pas de `#`, `^`, `[`, `]`, `|` dans un nom de note.

## Propriétés

Huit au plus, noms sans accent pour les requêtes et les agents :

| Propriété | Sens | Valeurs |
| --- | --- | --- |
| `projet` | le projet, en lien | `"[[Mon-appli]]"` |
| `type` | la nature de la note | projet, suivi, sommaire, discovery, cadrage, design, conception, ticket, qualite, decision, mise-en-ligne, journal, methode |
| `statut` | où en est la note | a-faire, brouillon, valide, obsolete |
| `agent` | qui écrit ce livrable | un profil Hermès, ou HUMAIN |
| `resume` | une ligne, lue avant d'ouvrir la note | texte |
| `haut` | le sommaire de sa section | lien |
| `precedent`, `suivant` | le fil de lecture du projet | liens |

La note projet a en plus `phase`, `depot` (propriétaire/dépôt GitHub), `prod` et `preprod`. L'avancement est calculé dans la note `<Nom> - GitHub`, générée et jamais versionnée.
Un ticket a `numero`, `issue` (adresse GitHub) et `branche` à la place de `agent`, `precedent` et `suivant`.

## Liens

- **Fil de lecture** : `precedent` et `suivant` relient toutes les notes d'un projet dans l'ordre, de la note projet jusqu'au journal. On peut lire un projet d'un bout à l'autre sans revenir au sommaire.
- **Sommaire par thème** : chaque note pointe vers le sommaire de sa section (`haut`), chaque sommaire vers la note projet.
- **Rétroliens** : Obsidian les calcule seul. Le panneau des rétroliens d'une note montre qui la cite, sans rien écrire en double.
- **Liens dans le texte** : citer la note d'origine plutôt que recopier son contenu. Une information vit à un seul endroit.

## Accès des agents

1. Un agent écrit son livrable dans la note dont la propriété `agent` porte son nom, et peut la relire.
2. Pour s'orienter, il lit d'abord la note projet, puis le `resume` des notes. Il n'ouvre une note que si son besoin la désigne : carte kanban parente, ou `resume` qui y répond.
3. Il ne lit jamais tout le vault, ni tout un projet.
4. Ce qui se demande à la machine ne se lit pas dans les notes : la date vient de `date`, l'état des tickets du récap généré.
5. Le vault personnel de PRENOM n'est jamais lu directement : il passe par l'agent gardien, à concevoir.

## Graphe

Couleurs conseillées (Graphe, réglages, Groupes) : `["type":projet]`, `["type":sommaire]`, `["type":ticket]`, `["type":decision]`, une couleur chacune. Exclure `_Modèles` du graphe (Réglages, Fichiers et liens, Fichiers exclus) pour ne pas mélanger le projet fictif aux vrais.
"""

ACCUEIL = """---
type: methode
statut: valide
resume: "Point d'entrée du vault Projets."
---

# Accueil

- [[00 Tableau de bord]] : où en est chaque projet.
- [[Conventions]] : nommage, propriétés, liens, accès des agents.

## Projets
![[Projets.base]]

## Documents à faire
Les notes encore vides, par projet.
![[Documents à faire.base]]

## Tickets
![[Tickets.base]]
"""

BASES = {
    "Projets.base": """filters:
  and:
    - note.type == "suivi"
    - '!file.inFolder("_Modèles")'
views:
  - type: table
    name: Projets
    order:
      - note.projet
      - note.avancement
      - file.name
""",
    "Tickets.base": """filters:
  and:
    - note.type == "ticket"
    - '!file.inFolder("_Modèles")'
    - '!file.inFolder("_À trier")'
views:
  - type: table
    name: Tickets par statut
    groupBy:
      property: note.statut
      direction: ASC
    order:
      - file.name
      - note.projet
      - note.numero
      - note.execution
      - note.branche
""",
    "Documents à faire.base": """filters:
  and:
    - note.statut == "a-faire"
    - '!file.inFolder("_Modèles")'
    - '!file.inFolder("_À trier")'
views:
  - type: table
    name: À faire par projet
    groupBy:
      property: note.projet
      direction: ASC
    order:
      - file.name
      - note.type
      - note.agent
      - note.resume
""",
}


def cmd_modele(_):
    n = generer_projet(VAULT / "_Modèles" / "Projet", "PROJET", "proprietaire/depot", ecraser=True)
    for nom, texte in MODELES_NOTES.items():
        texte = re.sub(r'^(projet|haut): ".*"$', r"\1:", texte, flags=re.M)
        n += ecrire(VAULT / "_Modèles" / "Notes" / f"{nom}.md", texte)
    methode = Path(__file__).resolve().parent.parent.parent / "methode"
    for src, dest in (("portes.md", VAULT / "_Méthode" / "Portes.md"),
                      ("modele-fiche-qa.md", VAULT / "_Modèles" / "Notes" / "Fiche QA.md")):
        if (methode / src).exists():
            corps = (methode / src).read_text(encoding="utf-8")
            entete = '---\ntype: methode\nstatut: valide\nresume: "Méthode commune du harness, livrée par le moteur."\n---\n\n'
            n += ecrire(dest, entete + corps)
    n += ecrire(VAULT / "_Méthode" / "Conventions.md", CONVENTIONS.replace("HUMAIN", HUMAIN).replace("PRENOM", PRENOM))
    for nom, texte in BASES.items():
        n += ecrire(VAULT / "_Méthode" / nom, texte)
    n += ecrire(VAULT / "00 Accueil.md", ACCUEIL)
    # vault neuf : un tableau de bord vide, remplacé au premier récap
    n += ecrire(VAULT / "00 Tableau de bord.md", '---\ntype: methode\nstatut: valide\nresume: "Généré : tous les projets et leur avancement."\n---\n\n# Tableau de bord\n\nRempli par `vault_projets.py recap`.\n', ecraser=False)
    print(f"modèle : {n} fichier(s) écrit(s)")


def cmd_completer(a):
    racine = VAULT / a.nom
    if not (racine / f"{a.nom}.md").exists():
        sys.exit(f"{racine} n'est pas un projet du vault.")
    print(f"{a.nom} : {generer_projet(racine, a.nom)} fichier(s) ajouté(s) ou remis en ordre")


def cmd_nouveau(a):
    racine = VAULT / a.nom
    if (racine / f"{a.nom}.md").exists():
        sys.exit(f"{racine} est déjà un projet : rien n'est écrasé (voir la commande completer).")
    print(f"{a.nom} : {generer_projet(racine, a.nom, a.depot)} fichier(s) créé(s) dans {racine}")


# ---------- récap depuis GitHub ----------

def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return json.loads(r.stdout or "null")


def lire_fm(texte):
    m = re.match(r"---\n(.*?)\n---\n", texte, re.S)
    fm = {}
    for ligne in (m.group(1).splitlines() if m else []):
        if ":" in ligne:
            k, v = ligne.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm


def statuts_tickets(depot):
    issues = gh("issue", "list", "-R", depot, "-s", "all", "-L", "500",
                "--json", "number,title,state,labels,url")
    prs = gh("pr", "list", "-R", depot, "-s", "all", "-L", "500",
             "--json", "number,title,state,headRefName,baseRefName,mergedAt,url")
    branches = {b["name"] for b in gh("api", f"repos/{depot}/branches?per_page=100")}
    sorties = sorted([p for p in prs if p["state"] == "MERGED" and p["headRefName"] == "preprod"
                      and p["baseRefName"] == "main"], key=lambda p: p["mergedAt"])
    tickets = []
    for i in sorted(issues, key=lambda x: x["number"]):
        n = i["number"]
        liees = [p for p in prs if f"#{n})" in p["title"] or p["headRefName"].startswith(f"{n}-")]
        fusion = sorted([p for p in liees if p["state"] == "MERGED"], key=lambda p: p["mergedAt"])
        t = {"n": n, "titre": i["title"], "url": i["url"], "labels": [l["name"] for l in i["labels"]],
             "pr": fusion[-1] if fusion else next((p for p in liees if p["state"] == "OPEN"), None)}
        t["branche"] = next((b for b in sorted(branches) if b.startswith(f"{n}-")), "")
        if fusion:
            p = fusion[-1]
            sortie = next((s for s in sorties if s["mergedAt"] >= p["mergedAt"]), None)
            if p["baseRefName"] == "main":
                t["statut"], t["date"] = "en-ligne", p["mergedAt"]
            elif sortie:
                t["statut"], t["date"] = "en-ligne", sortie["mergedAt"]
            else:
                t["statut"], t["date"] = "en-preprod", p["mergedAt"]
        elif any(p["state"] == "OPEN" for p in liees):
            t["statut"] = "en-revue"
        elif any(b.startswith(f"{n}-") for b in branches):
            t["statut"] = "en-cours"
        elif i["state"] == "CLOSED":
            t["statut"] = "ferme"
        else:
            t["statut"] = "a-faire"
        tickets.append(t)
    return tickets, prs, sorties


def court(texte, n=28):
    texte = re.sub(r"\s+", " ", re.sub(r'["`:;]', " ", texte)).strip()
    return texte if len(texte) <= n else texte[: n - 1].rstrip() + "…"


def graphe_branches(prs, tickets):
    """gitGraph Mermaid : main en bleu, preprod en vert, un point par ticket fusionné, une fusion par mise en ligne."""
    par_num = {t["n"]: t for t in tickets}
    evts = []
    for p in prs:
        if p["state"] != "MERGED":
            continue
        if p["headRefName"] == "preprod" and p["baseRefName"] == "main":
            evts.append((p["mergedAt"], "sortie", p))
        elif p["baseRefName"] in ("preprod", "main"):
            evts.append((p["mergedAt"], "ticket", p))
    evts.sort(key=lambda e: e[0])
    lignes = ["```mermaid",
              "%%{init: {'theme':'base','gitGraph':{'showCommitLabel':true,'rotateCommitLabel':true},"
              "'themeVariables':{'git0':'#3B6FD8','git1':'#22A447','git2':'#E0A100','git3':'#9B59B6',"
              "'commitLabelFontSize':'11px'}}}%%",
              "gitGraph", '  commit id:"Départ"', "  branch preprod"]
    vus, branche, attente = set(), "preprod", False
    for date, genre, p in evts:
        if genre == "sortie":
            if not attente:
                continue
            j = dt.datetime.fromisoformat(date.replace("Z", "+00:00")).strftime("%d/%m")
            ident = f"En ligne {j} (PR {p['number']})"
            lignes += ["  checkout main", f'  merge preprod id:"{ident}" tag:"en ligne"', "  checkout preprod"]
            attente = False
            continue
        m = re.match(r"(\d+)-", p["headRefName"]) or re.search(r"#(\d+)\)", p["title"])
        n = int(m.group(1)) if m else None
        etiquette = f"#{n} {court(par_num[n]['titre'])}" if n in par_num else f"PR {p['number']}"
        while etiquette in vus:
            etiquette += "·"
        vus.add(etiquette)
        if p["baseRefName"] == "main":
            lignes += ["  checkout main", f'  commit id:"{etiquette}" type:HIGHLIGHT', "  checkout preprod"]
        else:
            lignes.append(f'  commit id:"{etiquette}"')
            attente = True
    for t in tickets:
        if t["statut"] in ("en-cours", "en-revue"):
            b = f"{t['n']}-en-cours"
            lignes += [f"  branch {b}", f'  commit id:"#{t["n"]} {court(t["titre"])} ({STATUTS_TICKET[t["statut"]]})" type:REVERSE',
                       "  checkout preprod"]
    lignes.append("```")
    return "\n".join(lignes)


def note_ticket(nom, t, projet_dir):
    for f in (projet_dir / "05 Tickets").glob(f"{nom} - T{t['n']:02d} *.md"):
        return f"[[{f.stem}]] ([issue #{t['n']}]({t['url']}))"
    return f"[#{t['n']} {t['titre']}]({t['url']})"


def bloc_recap(nom, fm, projet_dir):
    depot = fm.get("depot", "")
    if not depot or "/" not in depot:
        return "Pas de dépôt GitHub renseigné (propriété `depot`).", 0, {}, []
    tickets, prs, sorties = statuts_tickets(depot)
    compte = collections.Counter(t["statut"] for t in tickets)
    actifs = [t for t in tickets if t["statut"] != "ferme"]
    faits = sum(1 for t in actifs if t["statut"] in ("en-ligne", "en-preprod"))
    pct = round(100 * faits / len(actifs)) if actifs else 0
    barre = "█" * (pct // 5) + "░" * (20 - pct // 5)
    gh_url = f"https://github.com/{depot}"
    maintenant = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    l = [f"## Suivi", "",
         f"*Généré le {maintenant} depuis [{depot}]({gh_url}). Ne pas modifier ce bloc à la main.*", "",
         f"**Avancement : {pct} %** `{barre}`", "",
         "| En ligne | En préprod | En revue | En cours | À faire |", "| --- | --- | --- | --- | --- |",
         f"| {compte['en-ligne']} | {compte['en-preprod']} | {compte['en-revue']} | {compte['en-cours']} | {compte['a-faire']} |", "",
         f"Liens : [dépôt]({gh_url}) · [issues]({gh_url}/issues) · [demandes de fusion]({gh_url}/pulls) · [branches]({gh_url}/branches)"]
    if fm.get("prod"):
        l[-1] += f" · [production]({fm['prod']})"
    if fm.get("preprod"):
        l[-1] += f" · [préproduction]({fm['preprod']})"
    groupes = [("En cours", ("en-revue", "en-cours")), ("À faire", ("a-faire",)),
               ("Faits", ("en-preprod", "en-ligne")), ("Fermés sans suite", ("ferme",))]
    for titre, statuts in groupes:
        liste = [t for t in tickets if t["statut"] in statuts]
        if not liste and titre == "Fermés sans suite":
            continue
        l += ["", f"### {titre} ({len(liste)})", ""]
        if not liste:
            l.append("Aucun.")
        for t in liste:
            etat = STATUTS_TICKET[t["statut"]]
            if t.get("date"):
                etat += " le " + t["date"][:10]
            pr = f" · [PR #{t['pr']['number']}]({t['pr']['url']})" if t.get("pr") else ""
            lab = f" `{', '.join(t['labels'])}`" if t["labels"] and t["labels"] != ["enhancement"] else ""
            l.append(f"- {note_ticket(nom, t, projet_dir)}{lab} : {etat}{pr}")
    l += ["", "### Branches et mises en ligne", "",
          "Bleu : `main`, la production. Vert : `preprod`. Chaque point vert est un ticket fusionné en préprod ; "
          "chaque retour sur la ligne bleue est une mise en ligne.", "", graphe_branches(prs, tickets)]
    if sorties:
        der = sorties[-1]
        l += ["", f"Dernière mise en ligne : [PR #{der['number']}]({der['url']}), le {der['mergedAt'][:10]}."]
    return "\n".join(l), pct, compte, tickets


def remplacer_bloc(texte, bloc):
    if DEBUT in texte and FIN in texte:
        return re.sub(re.escape(DEBUT) + r".*?" + re.escape(FIN), lambda _: f"{DEBUT}\n{bloc}\n{FIN}", texte, flags=re.S)
    return texte.rstrip() + f"\n\n{DEBUT}\n{bloc}\n{FIN}\n"


def actualiser_notes_autorisees(dossier, tickets):
    """Reporter le suivi GitHub sans recopier le contenu de la branche de code."""
    par_issue = {t["url"]: t for t in tickets}
    for note in dossier.glob("*.md"):
        if note.is_symlink():
            continue
        original = note.read_bytes()
        texte = original.decode("utf-8")
        fm = lire_fm(texte)
        ticket = par_issue.get(fm.get("issue"))
        if not ticket or fm.get("type") != "ticket" or fm.get("numero") != str(ticket["n"]):
            continue
        if fm.get("execution") != "À exécuter" or fm.get("statut") not in ("a-faire", "en-cours", "en-revue"):
            continue
        statut = {"en-cours": "en-cours", "en-revue": "en-revue", "en-preprod": "valide",
                  "en-ligne": "valide", "ferme": "obsolete"}.get(ticket["statut"])
        if not statut:
            continue
        entete, fin, corps = texte.partition("\n---\n")
        if not fin:
            continue
        pr = ticket.get("pr")
        champs = {"statut": statut}
        branche = pr["headRefName"] if pr else ticket.get("branche")
        if branche:
            champs["branche"] = json.dumps(branche, ensure_ascii=False)
        if pr:
            champs["pr"] = pr["url"]
        for cle, valeur in champs.items():
            motif = rf"^{cle}:.*$"
            if re.search(motif, entete, re.M):
                entete = re.sub(motif, lambda _: f"{cle}: {valeur}", entete, flags=re.M)
            else:
                entete += f"\n{cle}: {valeur}"
        resultat = (entete + fin + corps).encode("utf-8")
        if resultat == original:
            continue
        with tempfile.NamedTemporaryFile(dir=dossier, prefix=".suivi-", delete=False) as fichier:
            temp = Path(fichier.name)
            fichier.write(resultat)
        try:
            temp.chmod(note.stat().st_mode & 0o777)
            if note.read_bytes() == original:
                temp.replace(note)
        finally:
            temp.unlink(missing_ok=True)


def cmd_recap(_):
    lignes_tdb = []
    for f in sorted(VAULT.glob("*/*.md")):
        if f.stem != f.parent.name or f.parent.name.startswith(("_", ".")):
            continue
        texte = f.read_text(encoding="utf-8")
        fm = lire_fm(texte)
        try:
            bloc, pct, compte, tickets = bloc_recap(f.stem, fm, f.parent)
        except (RuntimeError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            # GitHub injoignable : on garde le dernier récap tel quel, et on le dit dans le journal
            print(f"{f.stem} : récap impossible, note GitHub laissée intacte ({type(e).__name__})")
            lignes_tdb.append(f"| [[{f.stem}]] | {fm.get('phase', '')} | Actualisation impossible | — | — | — | {fm.get('resume', '')} |")
            continue
        actualiser_notes_autorisees(f.parent / "05 Tickets", tickets)
        note_gh = f.parent / f"{f.stem} - GitHub.md"
        base = note_gh.read_text(encoding="utf-8") if note_gh.exists() else note_github(f.stem)
        neuf_gh = remplacer_bloc(base, bloc)
        if re.search(r"^avancement:", neuf_gh, re.M):
            neuf_gh = re.sub(r"^avancement:.*$", f"avancement: {pct}", neuf_gh, count=1, flags=re.M)
        else:
            neuf_gh = neuf_gh.replace("\n---\n", f"\navancement: {pct}\n---\n", 1)
        maj_gh = ecrire(note_gh, neuf_gh)
        print(f"{f.stem} : GitHub {'mis à jour' if maj_gh else 'inchangé'} ({pct} %)")
        lignes_tdb.append(f"| [[{f.stem}]] | {fm.get('phase', '')} | {pct} % | {compte.get('en-revue', 0) + compte.get('en-cours', 0)} | "
                          f"{compte.get('a-faire', 0)} | {compte.get('en-preprod', 0) + compte.get('en-ligne', 0)} | {fm.get('resume', '')} |")
    tdb = ["---", "type: methode", "statut: valide", 'resume: "Généré : tous les projets et leur avancement."', "---", "",
           "# Tableau de bord", "", f"*Généré le {dt.datetime.now():%Y-%m-%d %H:%M} par `vault_projets.py recap`.*", "",
           "| Projet | Phase | Avancement | En cours | À faire | Faits | En une phrase |",
           "| --- | --- | --- | --- | --- | --- | --- |", *lignes_tdb, "",
           "Vue détaillée : ![[Projets.base]]", "", "## Tickets du coffre", "", "![[Tickets.base]]", ""]
    print(f"tableau de bord : {'mis à jour' if ecrire(VAULT / '00 Tableau de bord.md', chr(10).join(tdb)) else 'inchangé'}")


# ---------- vérification ----------

def cmd_verifier(a):
    racine = Path(a.dossier) if a.dossier else VAULT
    if not racine.is_dir():
        sys.exit(f"Dossier à vérifier introuvable : {racine}")
    dossiers_profils = {section["dossier"] for section in SECTIONS if "profil_phase" in section}
    ignores = lambda p: (p.relative_to(racine).parts == ("AGENTS.md",)
                         or (p.name == "agent.md" and p.parent.name in dossiers_profils)
                         or any(x.startswith(".") or x in ("code", "_À trier", "node_modules") for x in p.relative_to(racine).parts))
    notes = [p for p in racine.rglob("*.md") if not ignores(p)]
    autres = {p.name.lower() for p in racine.rglob("*") if p.is_file() and p.suffix != ".md" and not ignores(p)}
    noms = collections.Counter(p.stem.lower() for p in notes)
    casses, manquantes, paragraphes = [], [], collections.defaultdict(set)
    for p in notes:
        texte = p.read_text(encoding="utf-8")
        sans_code = re.sub(r"```.*?```|`[^`\n]*`", "", texte, flags=re.S)
        for cible in re.findall(r"!?\[\[([^\]|#^]+)", sans_code):
            c = cible.strip().lower()
            if c not in noms and c not in autres and c.removesuffix(".md") not in noms:
                casses.append(f"{p.relative_to(racine)} -> [[{cible}]]")
        fm = lire_fm(texte)
        typ = fm.get("type")
        attendues = (["type", "statut", "phase", "depot"] if typ == "projet"
                     else ["projet", "type", "statut", "numero", "issue", "haut"] if typ == "ticket"
                     else ["projet", "type", "resume", "haut"] if typ == "suivi"
                     else ["type", "statut", "resume"] if typ == "methode" or "_Modèles/Notes" in str(p)
                     else PROPRIETES)
        # Les notes ajoutées en séance suivent les modèles courts (CR, décision,
        # entretien, atelier), sans le fil de lecture des notes du classeur.
        projet = p.parent.parent.name
        if p.parent.name in {section["dossier"] for section in SECTIONS} and typ in ("journal", "decision", "discovery"):
            titres = {titre for _, titre, _ in parcours(projet)}
            if p.stem not in titres:
                attendues = ["projet", "type", "statut", "resume", "haut"]
        if "source" in fm and "precedent" in attendues:
            attendues = ["source" if k == "precedent" else k for k in attendues]
        manque = [] if p.name in ("AGENTS.md", "CLAUDE.md", "LICENCES-TIERS.md", "README.md") else [k for k in attendues if k not in fm]  # fichiers de règles, pas des notes
        if manque:
            manquantes.append(f"{p.relative_to(racine)} : {', '.join(manque)}")
        if "_Modèles" not in str(p):
            corps = re.sub(r"---\n.*?\n---\n", "", texte, count=1, flags=re.S)
            for para in re.split(r"\n\s*\n", corps):
                para = para.strip()
                if len(para) > 120 and not para.startswith(("|", "<!--", "```", DEBUT)):
                    paragraphes[para].add(str(p.relative_to(racine)))
    doublons_noms = [n for n, c in noms.items() if c > 1]
    doublons_texte = [sorted(v) for v in paragraphes.values() if len(v) > 1]
    print(f"notes : {len(notes)}")
    for titre, liste in [("liens cassés", casses), ("propriétés manquantes", manquantes),
                         ("noms en double", doublons_noms), ("paragraphes en double", doublons_texte)]:
        print(f"{titre} : {len(liste)}")
        for x in liste[:15]:
            print(f"  - {x}")
    sys.exit(1 if casses or manquantes or doublons_noms or doublons_texte else 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("modele").set_defaults(f=cmd_modele)
    n = sp.add_parser("nouveau"); n.add_argument("nom"); n.add_argument("--depot", default=""); n.set_defaults(f=cmd_nouveau)
    c = sp.add_parser("completer"); c.add_argument("nom"); c.set_defaults(f=cmd_completer)
    sp.add_parser("recap").set_defaults(f=cmd_recap)
    v = sp.add_parser("verifier"); v.add_argument("dossier", nargs="?"); v.set_defaults(f=cmd_verifier)
    a = ap.parse_args()
    a.f(a)
