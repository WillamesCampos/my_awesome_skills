#!/usr/bin/env python3
"""Validate the deterministic artifacts of a LinkedIn post package."""

from __future__ import annotations

import argparse
import json
import struct
import subprocess
import zlib
from fractions import Fraction
from pathlib import Path
from typing import Any


REQUIRED_TEXT_FILES = (
    "brief.yaml",
    "fontes/material-estudado.md",
    "texto/versao-final.md",
    "visual/roteiro.md",
    "rastreabilidade.yaml",
)
EXPECTED_WIDTH = 1080
EXPECTED_HEIGHT = 1350
MIN_DURATION = 8.0
MAX_DURATION = 15.0


def _png_dimensions(path: Path) -> tuple[int, int]:
    content = path.read_bytes()
    if len(content) < 45 or content[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("arquivo não é um PNG válido")

    offset = 8
    dimensions: tuple[int, int] | None = None
    saw_iend = False
    chunk_index = 0
    while offset < len(content):
        if offset + 12 > len(content):
            raise ValueError("chunk PNG truncado")
        length = struct.unpack(">I", content[offset : offset + 4])[0]
        chunk_type = content[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(content):
            raise ValueError("dados de chunk PNG truncados")
        chunk_data = content[offset + 8 : offset + 8 + length]
        expected_crc = struct.unpack(">I", content[offset + 8 + length : chunk_end])[0]
        actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if expected_crc != actual_crc:
            raise ValueError("CRC inválido em chunk PNG")
        if chunk_index == 0:
            if chunk_type != b"IHDR" or length != 13:
                raise ValueError("primeiro chunk PNG deve ser IHDR")
            dimensions = struct.unpack(">II", chunk_data[:8])
        if chunk_type == b"IEND":
            if length != 0 or chunk_end != len(content):
                raise ValueError("chunk IEND inválido")
            saw_iend = True
            break
        offset = chunk_end
        chunk_index += 1

    if dimensions is None or not saw_iend:
        raise ValueError("estrutura PNG incompleta")
    return dimensions


def _probe_video(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "stream=width,height,r_frame_rate",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def validate_package(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    checks: list[dict[str, str]] = []
    errors: list[str] = []

    for relative in REQUIRED_TEXT_FILES:
        path = root / relative
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            errors.append(f"arquivo obrigatório ausente ou vazio: {relative}")
            checks.append({"check": relative, "result": "fail"})
        else:
            checks.append({"check": relative, "result": "pass"})

    cover = root / "output/capa.png"
    if not cover.is_file():
        errors.append("arquivo obrigatório ausente: output/capa.png")
        checks.append({"check": "cover", "result": "fail"})
    else:
        try:
            dimensions = _png_dimensions(cover)
            if dimensions != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
                errors.append(
                    "capa deve ter 1080x1350; "
                    f"encontrado {dimensions[0]}x{dimensions[1]}"
                )
                checks.append({"check": "cover", "result": "fail"})
            else:
                checks.append({"check": "cover", "result": "pass"})
        except (OSError, ValueError, struct.error) as error:
            errors.append(f"capa inválida: {error}")
            checks.append({"check": "cover", "result": "fail"})

    video = root / "output/post.mp4"
    if not video.is_file() or video.stat().st_size == 0:
        errors.append("arquivo obrigatório ausente ou vazio: output/post.mp4")
        checks.append({"check": "video", "result": "fail"})
    else:
        try:
            metadata = _probe_video(video)
            streams = metadata.get("streams", [])
            stream = streams[0] if streams else {}
            width = int(stream.get("width", 0))
            height = int(stream.get("height", 0))
            frame_rate = Fraction(str(stream.get("r_frame_rate", "0/1")))
            duration = float(metadata.get("format", {}).get("duration", 0))
            if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
                errors.append(
                    f"vídeo deve ter 1080x1350; encontrado {width}x{height}"
                )
            if not MIN_DURATION <= duration <= MAX_DURATION:
                errors.append(
                    "duração do vídeo deve estar entre 8 e 15 segundos; "
                    f"encontrado {duration:.2f}"
                )
            if frame_rate != 30:
                errors.append(
                    f"vídeo deve usar 30 fps; encontrado {float(frame_rate):g} fps"
                )
            checks.append(
                {
                    "check": "video",
                    "result": "pass"
                    if (width, height) == (EXPECTED_WIDTH, EXPECTED_HEIGHT)
                    and MIN_DURATION <= duration <= MAX_DURATION
                    and frame_rate == 30
                    else "fail",
                }
            )
        except FileNotFoundError:
            errors.append("ffprobe não está disponível; vídeo não foi validado")
            checks.append({"check": "video", "result": "pending"})
        except (subprocess.CalledProcessError, ValueError, TypeError, json.JSONDecodeError) as error:
            errors.append(f"não foi possível validar o vídeo com ffprobe: {error}")
            checks.append({"check": "video", "result": "fail"})

    return {
        "status": "APROVADO" if not errors else "PENDENTE",
        "checks": checks,
        "errors": errors,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("post_path", type=Path, help="Pasta absoluta do post")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    result = validate_package(args.post_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "APROVADO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
