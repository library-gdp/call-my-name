#!/usr/bin/env python3
"""Atomically publish a completed user-context Markdown draft."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path


def publish(draft: Path, output: Path) -> None:
    if draft.is_symlink():
        raise ValueError("draft must not be a symlink")
    draft = draft.resolve(strict=True)
    if not draft.is_file():
        raise ValueError("draft must be a regular file")
    content = draft.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError("draft is empty")

    output = output.resolve(strict=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=output.parent,
        prefix=f".{output.name}.",
        suffix=".tmp",
        delete=False,
    )
    temporary_path = Path(handle.name)
    try:
        with handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, output)
        if draft != output:
            draft.unlink()
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        publish(args.draft, args.output)
    except (OSError, ValueError) as error:
        print(f"failed to publish user context: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
