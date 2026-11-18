from __future__ import annotations

import importlib.util
import json
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "validate_post_package.py"
SPEC = importlib.util.spec_from_file_location("validate_post_package", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def write_png_header(path: Path, width: int, height: int) -> None:
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 8 + struct.pack(">II", width, height))


class ValidatePostPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        required_text = (
            "brief.yaml",
            "fontes/material-estudado.md",
            "texto/versao-final.md",
            "visual/roteiro.md",
            "rastreabilidade.yaml",
        )
        for relative in required_text:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("conteúdo verificado\n", encoding="utf-8")
        output = self.root / "output"
        output.mkdir()
        (output / "post.mp4").write_bytes(b"video")
        write_png_header(output / "capa.png", 1080, 1350)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    @staticmethod
    def valid_ffprobe(*args, **kwargs):
        payload = {
            "streams": [{"width": 1080, "height": 1350, "r_frame_rate": "30/1"}],
            "format": {"duration": "10.0"},
        }
        return type("Result", (), {"stdout": json.dumps(payload), "returncode": 0})()

    def test_complete_package_is_approved_without_gif(self) -> None:
        with patch.object(MODULE.subprocess, "run", side_effect=self.valid_ffprobe):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "APROVADO")
        self.assertEqual(result["errors"], [])

    def test_missing_final_text_is_pending(self) -> None:
        (self.root / "texto/versao-final.md").unlink()

        with patch.object(MODULE.subprocess, "run", side_effect=self.valid_ffprobe):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("texto/versao-final.md" in error for error in result["errors"]))

    def test_rejects_wrong_cover_dimensions(self) -> None:
        write_png_header(self.root / "output/capa.png", 1200, 1200)

        with patch.object(MODULE.subprocess, "run", side_effect=self.valid_ffprobe):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("capa" in error for error in result["errors"]))

    def test_rejects_video_outside_duration_range(self) -> None:
        def long_video(*args, **kwargs):
            payload = {
                "streams": [
                    {"width": 1080, "height": 1350, "r_frame_rate": "30/1"}
                ],
                "format": {"duration": "20.0"},
            }
            return type("Result", (), {"stdout": json.dumps(payload), "returncode": 0})()

        with patch.object(MODULE.subprocess, "run", side_effect=long_video):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("duração" in error for error in result["errors"]))

    def test_missing_ffprobe_is_pending(self) -> None:
        with patch.object(MODULE.subprocess, "run", side_effect=FileNotFoundError):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("ffprobe" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
