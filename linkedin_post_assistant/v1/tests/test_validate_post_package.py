from __future__ import annotations

import importlib.util
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "validate_post_package.py"
SPEC = importlib.util.spec_from_file_location("validate_post_package", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def write_png_header(path: Path, width: int, height: int) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    raw_scanline = b"\x00" + (b"\x00\x00\x00" * width)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk("IHDR".encode(), struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk("IDAT".encode(), zlib.compress(raw_scanline * height))
        + chunk("IEND".encode(), b"")
    )
    path.write_bytes(png)


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

    def test_missing_traceability_is_pending(self) -> None:
        (self.root / "rastreabilidade.yaml").unlink()

        with patch.object(MODULE.subprocess, "run", side_effect=self.valid_ffprobe):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("rastreabilidade.yaml" in error for error in result["errors"]))

    def test_missing_cover_is_pending(self) -> None:
        (self.root / "output/capa.png").unlink()

        with patch.object(MODULE.subprocess, "run", side_effect=self.valid_ffprobe):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("capa.png" in error for error in result["errors"]))

    def test_missing_video_is_pending(self) -> None:
        (self.root / "output/post.mp4").unlink()

        result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("post.mp4" in error for error in result["errors"]))

    def test_rejects_wrong_cover_dimensions(self) -> None:
        write_png_header(self.root / "output/capa.png", 1200, 1200)

        with patch.object(MODULE.subprocess, "run", side_effect=self.valid_ffprobe):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("capa" in error for error in result["errors"]))

    def test_rejects_truncated_png(self) -> None:
        (self.root / "output/capa.png").write_bytes(
            b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
        )

        with patch.object(MODULE.subprocess, "run", side_effect=self.valid_ffprobe):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("capa inválida" in error for error in result["errors"]))

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

    def test_rejects_video_with_wrong_frame_rate(self) -> None:
        def slow_frame_rate(*args, **kwargs):
            payload = {
                "streams": [
                    {"width": 1080, "height": 1350, "r_frame_rate": "24/1"}
                ],
                "format": {"duration": "10.0"},
            }
            return type("Result", (), {"stdout": json.dumps(payload), "returncode": 0})()

        with patch.object(MODULE.subprocess, "run", side_effect=slow_frame_rate):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("30 fps" in error for error in result["errors"]))

    def test_missing_ffprobe_is_pending(self) -> None:
        with patch.object(MODULE.subprocess, "run", side_effect=FileNotFoundError):
            result = MODULE.validate_package(self.root)

        self.assertEqual(result["status"], "PENDENTE")
        self.assertTrue(any("ffprobe" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
