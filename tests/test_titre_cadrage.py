import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/cadrage/scripts/titre.py"


class TitreCadrageTest(unittest.TestCase):
    def setUp(self):
        temporaire = TemporaryDirectory()
        self.addCleanup(temporaire.cleanup)
        self.vault = Path(temporaire.name)
        methode = self.vault / "_Méthode"
        methode.mkdir()
        (methode / "Conventions.md").touch()
        self.projet = self.vault / "Projet fictif"
        self.projet.mkdir()
        self.note = self.projet / "Projet fictif.md"
        self.note.write_text("---\nphase: 'discovery'\n---\n", encoding="utf-8")

    def lancer_hook(self, **champs):
        entree = {"cwd": str(self.projet), "prompt": "/cadrage", **champs}
        resultat = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps(entree),
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(resultat.stdout)["hookSpecificOutput"]["sessionTitle"] if resultat.stdout else None

    def test_lit_la_phase_du_classeur_au_lancement_et_a_la_reprise(self):
        self.assertEqual(self.lancer_hook(), "Discovery")
        self.note.write_text("---\nphase: conception\n---\n", encoding="utf-8")
        prompt = "Projet fictif.\nLancez le skill cadrage à la phase Conception."
        self.assertEqual(self.lancer_hook(prompt=prompt), "Conception")

    def test_preserve_un_titre_choisi_et_ignore_les_autres_demandes(self):
        self.assertIsNone(self.lancer_hook(session_title="Un titre choisi"))
        self.assertIsNone(self.lancer_hook(prompt="Modifiez cette note.\nDesign\nMerci."))
        self.assertIsNone(self.lancer_hook(cwd=str(self.vault)))
