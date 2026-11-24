import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch


OUTIL = Path(__file__).resolve().parents[1] / "scripts/vault/vault_projets.py"


class RacineVaultTest(unittest.TestCase):
    def test_priorite_environnement_machine_instance(self):
        with tempfile.TemporaryDirectory() as dossier:
            accueil = Path(dossier)
            instance = accueil / "instance.conf"
            instance.write_text("RACINE_PROJETS=/srv/projets\n", encoding="utf-8")
            locale = accueil / ".config/harness-local/harness.conf"
            locale.parent.mkdir(parents=True)
            locale.write_text("RACINE_PROJETS=/coffre-local\n", encoding="utf-8")
            with patch.object(Path, "home", return_value=accueil):
                with patch.dict(os.environ, {"HARNESS_CONF": str(instance), "VAULT_PROJETS": ""}):
                    outil = runpy.run_path(str(OUTIL))
                    racine = outil["racine_vault"]
                    self.assertEqual(racine(), Path("/coffre-local"))
                    os.environ["VAULT_PROJETS"] = "/coffre-essai"
                    self.assertEqual(racine(), Path("/coffre-essai"))
                    del os.environ["VAULT_PROJETS"]
                    locale.unlink()
                    self.assertEqual(racine(), Path("/srv/projets"))
