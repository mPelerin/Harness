"""Donne aux conversations Claude Code le titre de leur phase de cadrage."""

import argparse
import json
import os
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile


TITRES = {
    "discovery": "Discovery",
    "cadrage": "Cadrage",
    "design": "Design",
    "conception": "Conception",
}
EVENEMENT = "UserPromptSubmit"
OUVERTURE = re.compile(
    r"(?m)(?:\A\s*/cadrage(?:\s|$)"
    r"|\A\s*(?:(?:lancez|lance|on lance|continuer) (?:le |la )?)?"
    r"(?:discovery|cadrage|design|conception)[.!?]?\s*\Z"
    r"|^(?:lancez|lance|reprenez|reprends) le skill cadrage\b)"
)


def titre_conversation(entree):
    if entree.get("session_title") or not OUVERTURE.search(entree.get("prompt", "").lower()):
        return None

    dossier = Path(entree["cwd"]).resolve()
    for vault in dossier.parents:
        if (vault / "_Méthode/Conventions.md").is_file():
            nom = dossier.relative_to(vault).parts[0]
            note = (vault / nom / f"{nom}.md").read_text(encoding="utf-8")
            fin_proprietes = note.find("\n---\n", 3)
            if not note.startswith("---\n") or fin_proprietes == -1:
                return None
            proprietes = note[:fin_proprietes]
            phase = re.search(r"(?m)^phase:[ \t]*(\w+|['\"]\w+['\"])[ \t]*$", proprietes)
            return TITRES.get(phase[1].strip("'\"").lower()) if phase else None
    return None


def configurer_hook(action):
    dossier = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    reglages = (dossier / "settings.json").resolve()
    original = reglages.read_text(encoding="utf-8") if reglages.exists() else None
    configuration = json.loads(original) if original is not None else {}
    commande = 'python3 "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/cadrage/scripts/titre.py"'
    entree = {"hooks": [{"type": "command", "command": commande}]}
    hooks = configuration.setdefault("hooks", {}).setdefault(EVENEMENT, [])
    if action == "--installer":
        if entree in hooks:
            return
        hooks.append(entree)
    elif entree in hooks:
        hooks.remove(entree)
    else:
        return

    temporaire = None
    try:
        with NamedTemporaryFile(dir=reglages.parent, mode="w", encoding="utf-8", delete=False) as fichier:
            temporaire = Path(fichier.name)
            json.dump(configuration, fichier, indent=2, ensure_ascii=False)
            fichier.write("\n")
        courant = reglages.read_text(encoding="utf-8") if reglages.exists() else None
        if courant != original:
            raise RuntimeError("Les réglages Claude Code ont changé pendant la mise à jour.")
        temporaire.replace(reglages)
    finally:
        if temporaire is not None:
            temporaire.unlink(missing_ok=True)


if __name__ == "__main__":
    analyseur = argparse.ArgumentParser(description=__doc__)
    actions = analyseur.add_mutually_exclusive_group()
    actions.add_argument("--installer", dest="action", action="store_const", const="--installer")
    actions.add_argument("--retirer", dest="action", action="store_const", const="--retirer")
    arguments = analyseur.parse_args()
    if arguments.action:
        configurer_hook(arguments.action)
    else:
        try:
            titre = titre_conversation(json.load(sys.stdin))
        except (KeyError, OSError, ValueError):
            titre = None
        if titre:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": EVENEMENT, "sessionTitle": titre}}))
