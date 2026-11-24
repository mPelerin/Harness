import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/orchestrateur.sh"


class OrchestrateurTest(unittest.TestCase):
    def test_la_cle_reste_identique_apres_un_changement_de_jour(self):
        with TemporaryDirectory() as chemin:
            dossier = Path(chemin)
            hermes = dossier / "hermes-fictif"
            hermes.write_text(
                """#!/usr/bin/env bash
while [ "$1" != --idempotency-key ]; do shift; done
printf '%s\n' "$2" >> "$CLES_HERMES_TEST"
cat >/dev/null
printf '{"id":"t_123abc"}\n'
""",
                encoding="utf-8",
            )
            horloge = dossier / "date"
            horloge.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$DATE_HERMES_TEST"\n', encoding="utf-8")
            for executable in (hermes, horloge):
                executable.chmod(0o700)
            conf = dossier / "harness.conf"
            conf.write_text(f"ORCHESTRATEUR={hermes}\n", encoding="utf-8")
            corps = dossier / "ticket.md"
            corps.write_text("Ticket fictif.\n", encoding="utf-8")
            cles = dossier / "cles"
            env = {**os.environ, "HARNESS_CONF": str(conf), "CLES_HERMES_TEST": str(cles),
                   "PATH": f"{dossier}{os.pathsep}{os.environ['PATH']}"}
            for date, depot in (("2026-01-10", "Equipe/Projet"), ("2026-01-11", "equipe/projet")):
                retour = subprocess.run(
                    ["bash", str(SCRIPT), "deposer-demande", "--ticket", "12", "--depot", depot,
                     "--titre", "Ticket fictif", "--corps", str(corps)],
                    env={**env, "DATE_HERMES_TEST": date}, capture_output=True, text=True, check=True,
                )
                self.assertEqual(retour.stdout.strip(), "t_123abc")
            premier, second = cles.read_text(encoding="utf-8").splitlines()
            self.assertEqual(premier, second)
