from pathlib import Path
import unittest


class TailleCadrageTest(unittest.TestCase):
    def test_le_skill_de_cadrage_tient_en_200_lignes(self):
        skill = Path(__file__).resolve().parents[1] / "skills/cadrage/SKILL.md"
        nombre_de_lignes = len(skill.read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(nombre_de_lignes, 200)
