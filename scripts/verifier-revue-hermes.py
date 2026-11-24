#!/usr/bin/env python3
"""Vérifie la revue Kanban du commit présenté à la livraison."""

import argparse
from contextlib import closing
import json
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys


NOM = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]*")
COMMIT = re.compile(r"[a-f0-9]{40}")


class RevueRefusee(ValueError):
    """Raison publiable de l'arrêt de la livraison."""


def metadata(run):
    valeur = run.get("metadata")
    if isinstance(valeur, str):
        valeur = json.loads(valeur)
    return valeur if isinstance(valeur, dict) else {}


def verifier_session(home, profil, session, fournisseur):
    if not isinstance(profil, str) or not NOM.fullmatch(profil):
        raise RevueRefusee("profil Kanban invalide")
    if not isinstance(session, str) or not NOM.fullmatch(session):
        raise RevueRefusee("session du profil non prouvée")
    base = home / "profiles" / profil / "state.db"
    try:
        with closing(sqlite3.connect(base.resolve().as_uri() + "?mode=ro", uri=True, timeout=3)) as db:
            route = db.execute(
                "SELECT model, billing_provider, api_call_count FROM sessions WHERE id = ?",
                (session,),
            ).fetchone()
    except sqlite3.Error:
        raise RevueRefusee("preuve de session Hermès indisponible") from None
    if not route or not route[0] or route[1] != fournisseur or (route[2] or 0) < 1:
        raise RevueRefusee("appel du fournisseur attendu non prouvé pour " + profil)


def verifier(carte, identifiant, commit, relecteur, fournisseur, fournisseur_code, home):
    fiche = carte["task"]
    if fiche.get("id") != identifiant or fiche.get("status") != "done":
        raise RevueRefusee("carte de code sans revue terminée")
    if fiche.get("model_override") or fiche.get("provider_override"):
        raise RevueRefusee("modèle ou fournisseur imposé sur la carte")
    passages = sorted(carte.get("runs") or [], key=lambda run: run["id"])
    if len(passages) < 2:
        raise RevueRefusee("passage du codeur ou du relecteur absent")
    code, revue = passages[-2:]
    if code.get("outcome") != "review_requested" or not code.get("profile"):
        raise RevueRefusee("demande de revue du codeur absente")
    if (
        revue.get("outcome") != "completed"
        or revue.get("profile") != relecteur
        or code["profile"] == relecteur
    ):
        raise RevueRefusee("verdict du relecteur indépendant absent")
    demande, verdict = metadata(code), metadata(revue)
    if verdict.get("review_outcome") != "approved":
        raise RevueRefusee("approbation explicite absente")
    if demande.get("commit") != commit or verdict.get("commit") != commit:
        raise RevueRefusee("le verdict ne porte pas sur le commit à livrer")
    verifier_session(home, code["profile"], demande.get("worker_session_id"), fournisseur_code)
    verifier_session(home, relecteur, verdict.get("worker_session_id"), fournisseur)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", required=True, help="tableau de la carte de code")
    parser.add_argument("--reviewer", required=True, help="profil de revue attendu")
    parser.add_argument("--provider", required=True, help="fournisseur du relecteur")
    parser.add_argument("--code-provider", required=True, help="fournisseur du codeur")
    parser.add_argument("--home", type=Path, default=Path.home() / ".hermes", help="racine des profils")
    parser.add_argument("card", help="identifiant de la carte de code")
    parser.add_argument("commit", help="SHA entier du commit à livrer")
    args = parser.parse_args()
    noms = (args.board, args.reviewer, args.card, args.provider, args.code_provider)
    if not all(NOM.fullmatch(v) for v in noms) or not COMMIT.fullmatch(args.commit):
        parser.error("tableau, profil, carte ou commit invalide")
    if args.provider == args.code_provider:
        parser.error("le codeur et le relecteur doivent utiliser des fournisseurs distincts")
    hermes = shutil.which("hermes") or str(Path.home() / ".local/bin/hermes")
    try:
        resultat = subprocess.run(
            [hermes, "kanban", "--board", args.board, "show", args.card, "--json"],
            capture_output=True, text=True, check=True, timeout=20,
        )
        verifier(
            json.loads(resultat.stdout), args.card, args.commit, args.reviewer,
            args.provider, args.code_provider, args.home,
        )
    except RevueRefusee as exc:
        print(f"Revue Hermès bloquée — {exc}", file=sys.stderr)
        return 1
    except (OSError, subprocess.SubprocessError, KeyError, TypeError, AttributeError, ValueError):
        print("Revue Hermès bloquée — preuve Kanban illisible ou inaccessible", file=sys.stderr)
        return 1
    print(f"Revue Hermès OK — {args.card} — {args.reviewer} — {args.commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
