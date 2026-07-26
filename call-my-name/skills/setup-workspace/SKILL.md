---
name: setup-workspace
description: Initialize or set up the current workspace for the call-my-name plugin by creating only the user-managed input paths required by the installed skills. Use when a first-time user asks to 초기 설정, 환경 설정, 작업공간 준비, 디렉터리 생성, 입력 파일 생성, setup, initialize, or bootstrap call-my-name.
---

# 작업공간 초기 설정

`call-my-name` 워크플로우를 시작하는 데 필요한 사용자 입력 경로만 준비하라. 후속 Skill이 관리하는 내부 데이터는 미리 만들지 마라.

## 실행 전 확인

1. 사용자가 `call-my-name`을 실행할 작업공간의 루트를 `WORKSPACE_ROOT`로 확정하라.
2. 이 Skill이 설치된 디렉터리를 `SKILL_DIR`로 두고 `SKILL_DIR/scripts/setup_workspace.py`가 있는지 확인하라.
3. `python3 --version`을 실행하라. Python이 설치되어 있지 않거나 실행되지 않으면 스크립트와 초기화 대상 파일을 만들거나 바꾸지 말고 아래 설치 안내를 제공한 뒤 종료하라.
   - 현재 운영체제와 패키지 관리자를 확인할 수 있으면 실제 설치 명령, 명령 실행 후 필요한 셸 재시작 또는 `PATH` 적용 방법, `python3 --version` 확인 명령을 순서대로 설명하라.
   - 운영체제나 패키지 관리자를 확정할 수 없으면 임의의 설치 명령을 제시하지 말고 `https://www.python.org/downloads/`를 안내하라.
   - 설치 후 `python3 --version`을 다시 실행해 달라고 요청하라.
4. 스크립트가 없으면 설치가 불완전한 상태이므로 작업공간을 변경하지 말고 플러그인 재설치 또는 관리자 확인을 요청하라.

## 초기화

다음 명령으로 버전 관리되는 초기화 스크립트를 실행하라.

```text
python3 "$SKILL_DIR/scripts/setup_workspace.py" "$WORKSPACE_ROOT"
```

스크립트는 다음 계약을 지켜야 한다.

- `src/user-info/`와 `src/jobs/`를 만들고, `src/jobs/JOB_SEEKER.md`가 없을 때만 채용공고 URL 입력 템플릿을 만든다.
- 기존 `JOB_SEEKER.md`의 내용은 바꾸지 않는다.
- `src/user-info/`에는 사용자가 이력서, 경력기술서, 포트폴리오 같은 분석 자료를 직접 추가하게 한다.
- `__workspace__/` 아래의 파일과 디렉터리는 후속 Skill이 워크플로우 중 자동으로 만들므로 생성하지 않는다.
- 사용자 작업공간의 `.gitignore`를 만들거나 수정하지 않는다.

## 유지보수와 완료 보고

- 플러그인 릴리스 개발 중 사용자 관리 입력 경로가 추가되거나 바뀌면 해당 Skill의 경로 계약과 `scripts/setup_workspace.py`를 같은 변경에서 갱신하고 실행 검증하라. 설치된 플러그인이 런타임에 스스로 스크립트를 수정하게 하지 마라.
- 완료 후 새로 생성한 경로와 그대로 보존한 경로를 구분해 보고하라.
- `__workspace__/`와 `.gitignore`를 건드리지 않았음을 확인하고, 사용자가 다음으로 `src/user-info/`에 자료를 넣거나 `src/jobs/JOB_SEEKER.md`에 공개 채용공고 URL을 추가할 수 있다고 안내하라.
