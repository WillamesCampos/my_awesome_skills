#!/usr/bin/env python3
"""Create a collision-safe workspace for one LinkedIn post."""

from __future__ import annotations

import argparse
import re
import unicodedata
from datetime import date
from pathlib import Path


DEFAULT_ROOT = Path.home() / "Documents" / "Posts"


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")
    if not slug:
        raise ValueError("título não gera um slug válido")
    return slug


def _next_available_path(root: Path, slug: str, run_date: date) -> Path:
    direct = root / slug
    if not direct.exists():
        return direct

    dated_slug = f"{slug}-{run_date.isoformat()}"
    dated = root / dated_slug
    if not dated.exists():
        return dated

    counter = 2
    while True:
        candidate = root / f"{dated_slug}-{counter}"
        if not candidate.exists():
            return candidate
        counter += 1


def create_workspace(title: str, root: Path, run_date: date) -> Path:
    root = root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    workspace = _next_available_path(root, slugify(title), run_date)
    workspace.mkdir(exist_ok=False)

    directories = (
        "fontes",
        "texto",
        "visual/assets",
        "visual/projeto-remotion",
        "output",
    )
    for relative in directories:
        (workspace / relative).mkdir(parents=True, exist_ok=False)

    files = {
        "brief.yaml": (
            f'title: "{title.replace(chr(34), chr(39))}"\n'
            f'date: "{run_date.isoformat()}"\n'
            'angle: ""\n'
            'case_type: ""\n'
            'editorial_state: "draft"\n'
        ),
        "fontes/material-estudado.md": "# Material estudado\n\n",
        "fontes/referencias.md": "# Referências verificadas\n\n",
        "texto/rascunho.md": "# Rascunho\n\n",
        "texto/versao-final.md": "# Versão final\n\n",
        "visual/roteiro.md": "# Roteiro visual\n\n",
        "rastreabilidade.yaml": (
            "claims: []\n"
            "pending_verification: []\n"
            "removed_confidential_details: []\n"
            'status: "PENDENTE"\n'
        ),
    }
    for relative, content in files.items():
        (workspace / relative).write_text(content, encoding="utf-8")

    return workspace


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Título humano da publicação")
    parser.add_argument(
        "--date",
        dest="run_date",
        type=date.fromisoformat,
        default=date.today(),
        help="Data em YYYY-MM-DD (padrão: hoje)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"Raiz dos posts (padrão: {DEFAULT_ROOT})",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    workspace = create_workspace(args.title, args.root, args.run_date)
    print(workspace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
