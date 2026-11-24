import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


OUTIL = Path(__file__).resolve().parents[1] / "scripts/vault/vault_projets.py"


class ProfilsPhasesTest(unittest.TestCase):
    def test_le_modele_alimente_le_projet_sans_ecraser_ses_profils(self):
        with TemporaryDirectory() as dossier:
            vault = Path(dossier)

            def lancer(*arguments):
                resultat = subprocess.run(
                    [sys.executable, str(OUTIL), *arguments],
                    env={**os.environ, "VAULT_PROJETS": dossier, "HARNESS_CONF": str(vault / "absent.conf")},
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(resultat.returncode, 0, resultat.stdout + resultat.stderr)

            modele = vault / "_Modèles" / "Projet"
            lancer("modele")
            attendus = {
                "01 Discovery": "product-manager",
                "02 Cadrage": "cpo",
                "03 Design": "ux-designer",
                "04 Conception": "technical-architect",
            }
            profils = {p.parent.name: p for p in modele.glob("*/agent.md")}
            self.assertEqual(profils.keys(), attendus.keys())
            for phase, role in attendus.items():
                self.assertIn(role, profils[phase].read_text(encoding="utf-8"))
            profils["01 Discovery"].write_text("Profil du modèle personnalisé.\n", encoding="utf-8")

            projet = vault / "Projet fictif"
            lancer("nouveau", projet.name)
            discovery = projet / "01 Discovery" / "agent.md"
            self.assertEqual(discovery.read_text(encoding="utf-8"), "Profil du modèle personnalisé.\n")
            discovery.write_text("Profil de ce projet.\n", encoding="utf-8")
            design = projet / "03 Design" / "agent.md"
            design.unlink()
            lancer("completer", projet.name)
            self.assertEqual(discovery.read_text(encoding="utf-8"), "Profil de ce projet.\n")
            self.assertEqual(design.read_bytes(), profils["03 Design"].read_bytes())
            lancer("verifier", str(projet))
