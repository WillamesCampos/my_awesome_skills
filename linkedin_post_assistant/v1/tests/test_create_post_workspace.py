from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import date
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "create_post_workspace.py"
SPEC = importlib.util.spec_from_file_location("create_post_workspace", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CreatePostWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_slugifies_accents_and_punctuation(self) -> None:
        self.assertEqual(
            MODULE.slugify("Por que EXPLAIN não basta?"),
            "por-que-explain-nao-basta",
        )

    def test_rejects_title_without_ascii_content(self) -> None:
        with self.assertRaisesRegex(ValueError, "título não gera um slug válido"):
            MODULE.slugify("🔥🔥")

    def test_creates_complete_package_tree(self) -> None:
        workspace = MODULE.create_workspace(
            "N+1 no Django", self.root, date(2026, 11, 18)
        )

        expected_files = {
            "brief.yaml",
            "fontes/material-estudado.md",
            "fontes/referencias.md",
            "texto/rascunho.md",
            "texto/versao-final.md",
            "visual/roteiro.md",
            "rastreabilidade.yaml",
        }
        expected_directories = {
            "visual/assets",
            "visual/projeto-remotion",
            "output",
        }

        self.assertTrue(all((workspace / item).is_file() for item in expected_files))
        self.assertTrue(
            all((workspace / item).is_dir() for item in expected_directories)
        )

    def test_existing_title_uses_date_without_overwrite(self) -> None:
        first = MODULE.create_workspace(
            "N+1 no Django", self.root, date(2026, 11, 18)
        )
        marker = first / "keep.txt"
        marker.write_text("preserve", encoding="utf-8")

        second = MODULE.create_workspace(
            "N+1 no Django", self.root, date(2026, 11, 18)
        )

        self.assertNotEqual(first, second)
        self.assertEqual(second.name, "n-1-no-django-2026-11-18")
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")

    def test_repeated_collision_adds_counter(self) -> None:
        MODULE.create_workspace("N+1", self.root, date(2026, 11, 18))
        MODULE.create_workspace("N+1", self.root, date(2026, 11, 18))

        third = MODULE.create_workspace("N+1", self.root, date(2026, 11, 18))

        self.assertEqual(third.name, "n-1-2026-11-18-2")


if __name__ == "__main__":
    unittest.main()
