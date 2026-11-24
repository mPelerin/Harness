from contextlib import closing
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/verifier-revue-hermes.py"
SPEC = importlib.util.spec_from_file_location("verifier_revue_hermes", SCRIPT)
REVUE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REVUE)
SHA = "a" * 40
CODEUR = "backend-engineer"
FOURNISSEUR_CODE = "fournisseur-code"
FOURNISSEUR_REVUE = "fournisseur-revue"


class VerifierRevueHermesTest(unittest.TestCase):
    def setUp(self):
        temporaire = tempfile.TemporaryDirectory()
        self.addCleanup(temporaire.cleanup)
        self.home = Path(temporaire.name)
        self.session(CODEUR, "session-code", "modele-code", FOURNISSEUR_CODE)
        self.session("reviewer", "session-revue", "modele-revue", FOURNISSEUR_REVUE)
        self.carte = {
            "task": {"id": "t_test", "status": "done"},
            "runs": [
                {"id": 1, "profile": CODEUR, "outcome": "review_requested", "metadata": {}},
                {"id": 2, "profile": "reviewer", "outcome": "changes_requested", "metadata": {}},
                {"id": 3, "profile": CODEUR, "outcome": "review_requested",
                 "metadata": {"commit": SHA, "worker_session_id": "session-code"}},
                {"id": 4, "profile": "reviewer", "outcome": "completed", "metadata": {
                    "commit": SHA, "review_outcome": "approved", "worker_session_id": "session-revue",
                }},
            ],
        }

    def session(self, profil, identifiant, model, fournisseur, appels=1):
        folder = self.home / "profiles" / profil
        folder.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(folder / "state.db")) as conn, conn:
            conn.execute("CREATE TABLE IF NOT EXISTS sessions "
                         "(id TEXT PRIMARY KEY, model TEXT, billing_provider TEXT, api_call_count INTEGER)")
            conn.execute("INSERT OR REPLACE INTO sessions VALUES (?, ?, ?, ?)",
                         (identifiant, model, fournisseur, appels))

    def verifier(self, sha=SHA):
        REVUE.verifier(self.carte, "t_test", sha, "reviewer", FOURNISSEUR_REVUE, FOURNISSEUR_CODE, self.home)

    def test_approuve_le_commit_corrige_et_ses_deux_sessions(self):
        self.carte["runs"][-1]["metadata"] = json.dumps(self.carte["runs"][-1]["metadata"])
        self.verifier()

    def test_refuse_un_sha_different(self):
        with self.assertRaisesRegex(REVUE.RevueRefusee, "commit à livrer"):
            self.verifier("b" * 40)
        self.carte["runs"][-2]["metadata"]["commit"] = "b" * 40
        with self.assertRaisesRegex(REVUE.RevueRefusee, "commit à livrer"):
            self.verifier()

    def test_refuse_un_autre_relecteur_ou_un_verdict_manquant(self):
        verdict = self.carte["runs"][-1]
        verdict["profile"] = CODEUR
        with self.assertRaisesRegex(REVUE.RevueRefusee, "relecteur indépendant"):
            self.verifier()
        verdict["profile"] = "reviewer"
        verdict["metadata"].pop("review_outcome")
        with self.assertRaisesRegex(REVUE.RevueRefusee, "approbation explicite"):
            self.verifier()

    def test_refuse_une_revue_active_ou_une_carte_surchargee(self):
        self.carte["task"]["status"] = "review"
        with self.assertRaisesRegex(REVUE.RevueRefusee, "revue terminée"):
            self.verifier()
        self.carte["task"].update(status="done", provider_override="autre")
        with self.assertRaisesRegex(REVUE.RevueRefusee, "imposé sur la carte"):
            self.verifier()

    def test_refuse_un_fournisseur_de_repli_ou_une_session_sans_appel(self):
        self.session("reviewer", "session-revue", "autre-modele", "autre-fournisseur")
        with self.assertRaisesRegex(REVUE.RevueRefusee, "fournisseur attendu"):
            self.verifier()
        self.session("reviewer", "session-revue", "modele-revue", FOURNISSEUR_REVUE, appels=0)
        with self.assertRaisesRegex(REVUE.RevueRefusee, "fournisseur attendu"):
            self.verifier()


if __name__ == "__main__":
    unittest.main()
