#!/usr/bin/env python3
"""call-my-name 사용자가 직접 관리하는 입력 경로를 초기화한다."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


JOB_SEEKER_TEMPLATE = """# 채용공고 URL

지원하려는 공개 채용공고 URL을 한 줄에 하나씩 추가하세요.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="call-my-name 사용자 입력 경로를 초기화합니다."
    )
    parser.add_argument(
        "workspace_root",
        type=Path,
        help="call-my-name을 실행할 기존 작업공간의 루트",
    )
    return parser.parse_args()


def require_directory(path: Path, label: str) -> None:
    if path.is_symlink():
        raise ValueError(f"{label}에 심볼릭 링크를 사용할 수 없습니다: {path}")
    if path.exists() and not path.is_dir():
        raise ValueError(f"{label} 경로가 디렉터리가 아닙니다: {path}")


def initialize(workspace_root: Path) -> tuple[list[Path], list[Path]]:
    if not workspace_root.exists():
        raise ValueError(f"작업공간이 존재하지 않습니다: {workspace_root}")
    if not workspace_root.is_dir():
        raise ValueError(f"작업공간이 디렉터리가 아닙니다: {workspace_root}")

    src_dir = workspace_root / "src"
    user_info_dir = src_dir / "user-info"
    jobs_dir = src_dir / "jobs"
    job_seeker_file = jobs_dir / "JOB_SEEKER.md"

    require_directory(src_dir, "src")
    require_directory(user_info_dir, "src/user-info")
    require_directory(jobs_dir, "src/jobs")

    created: list[Path] = []
    preserved: list[Path] = []

    for directory in (src_dir, user_info_dir, jobs_dir):
        if directory.exists():
            preserved.append(directory)
        else:
            directory.mkdir()
            created.append(directory)

    try:
        with job_seeker_file.open("x", encoding="utf-8", newline="\n") as file:
            file.write(JOB_SEEKER_TEMPLATE)
        created.append(job_seeker_file)
    except FileExistsError:
        if job_seeker_file.is_dir():
            raise ValueError(
                f"파일을 만들 위치에 디렉터리가 존재합니다: {job_seeker_file}"
            ) from None
        preserved.append(job_seeker_file)

    return created, preserved


def display_path(path: Path, workspace_root: Path) -> str:
    return str(path.relative_to(workspace_root))


def main() -> int:
    args = parse_args()
    workspace_root = args.workspace_root.expanduser()

    try:
        created, preserved = initialize(workspace_root)
    except (OSError, ValueError) as error:
        print(f"초기 설정 실패: {error}", file=sys.stderr)
        return 1

    for path in created:
        print(f"생성: {display_path(path, workspace_root)}")
    for path in preserved:
        print(f"유지: {display_path(path, workspace_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
