# `call-my-name` 아키텍처

## 1. 범위와 배포 단위

`call-my-name`은 지원자 자료와 공개 채용공고를 근거로 사용자 프로필을 구성하고 한국어 자기소개서 작성을 지원하는 Codex 플러그인이다. 저장소 전체가 아니라 `call-my-name/` 디렉터리만 설치·배포한다.

현재 배포물은 다음 요소로 구성된다.

```text
call-my-name/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    ├── setup-workspace/
    ├── parse-document-files/
    ├── collect-user-context/
    ├── review-user-profile/
    ├── collect-job/
    └── write-korean-cover-letter/
```

`AGENTS.md`, `.agents/`, `.codex/`, `docs/`, `__workspace__/`는 저장소 개발 자산이므로 플러그인 배포물에 포함하지 않는다. 플러그인이 사용자 작업공간에서 실행되면서 만드는 `__workspace__/`도 배포 디렉터리와는 별개의 런타임 데이터다.

## 2. 설계 개요

플러그인은 별도의 상주 서비스나 애플리케이션 서버 없이 Codex가 필요에 따라 선택하는 Skill 집합으로 동작한다. 각 Skill의 `SKILL.md`가 트리거 조건, 입력·출력 계약, 처리 절차와 안전 정책을 정의한다. `agents/openai.yaml`은 사용자에게 표시할 이름·설명과 기본 프롬프트를 제공하고, 상세 형식 계약은 `references/`, 결정적인 로컬 작업은 `scripts/`에 둔다.

구현은 두 계층으로 나뉜다.

- 구성 가능한 파이프라인: 작업공간 초기화, 문서 파싱, 사용자 컨텍스트 수집·검토, 채용공고 원문 수집을 각각 독립 Skill로 제공한다.
- 통합 작성 Skill: `write-korean-cover-letter`가 프로필 구축, 현재 공고 탐색·비교, 기업 조사와 자기소개서 작성을 요청 범위에 맞춰 수행한다.

현재 파이프라인 Skill 사이에는 프로세스 수준의 직접 호출이나 중앙 오케스트레이터가 없다. Codex가 Skill 계약과 작업공간의 파일을 통해 다음 단계를 연결한다. 예외적으로 `collect-user-context`는 비텍스트 문서를 읽을 때 `parse-document-files`를 명시적으로 사용한다.

## 3. 런타임 작업공간과 데이터 흐름

플러그인은 설치 위치와 사용자의 실행 작업공간을 분리한다. 모든 런타임 경로는 사용자가 플러그인을 실행하는 `WORKSPACE_ROOT`를 기준으로 해석한다.

```text
WORKSPACE_ROOT/
├── src/                              # 사용자가 관리하는 입력
│   ├── user-info/                    # 이력서·경력기술서·포트폴리오 등
│   └── jobs/
│       └── JOB_SEEKER.md             # 공개 채용공고 URL 목록
├── __workspace__/agent/              # Skill이 관리하는 중간 산출물
│   ├── USER_INSPECTION.md            # 구조화된 지원자 프로필
│   ├── jobs/                          # 공고별 원문 Markdown
│   └── parse-document-files-venv/    # 문서 파싱용 격리 Python 환경
└── USER_INSPECTION_*.md              # 수동 검토 중에만 쓰는 임시 파일
```

주요 흐름은 다음과 같다.

```text
setup-workspace
  ├─> src/user-info/ ─> collect-user-context ─> USER_INSPECTION.md
  │                         └─> parse-document-files
  │                                  (PDF·DOCX·XLSX·PPTX)
  │
  │                    USER_INSPECTION.md ─> review-user-profile
  │                                                └─> 같은 파일을 검증 후 교체
  │
  └─> src/jobs/JOB_SEEKER.md ─> collect-job ─> __workspace__/agent/jobs/*.md

사용자 자료 + 공개 웹의 현재 공고·기업 정보
  └─> write-korean-cover-letter ─> 프로필 요약·공고 비교·자기소개서 응답
```

`src/`는 사용자 입력 영역이며 초기화 이후 플러그인이 내용을 소유하지 않는다. `__workspace__/agent/`는 후속 Skill이 재사용하는 내부 산출물 영역이다. `setup-workspace`는 내부 산출물을 미리 만들지 않으며 `.gitignore`도 변경하지 않는다.

## 4. Skill 구성

| 영역 | Skill | 책임 | 입력 | 출력 또는 효과 |
| --- | --- | --- | --- | --- |
| 기반 | `setup-workspace` | 사용자 입력 경로를 멱등적으로 초기화 | `WORKSPACE_ROOT` | `src/user-info/`, `src/jobs/`, 없는 경우에만 `JOB_SEEKER.md` 생성 |
| 기반 | `parse-document-files` | 비텍스트 문서에서 위치가 있는 원문 텍스트 추출 | 호출 Skill이 지정한 PDF·DOCX·XLSX·PPTX 등 | 파일별 `source_file`, `units[].locator`, `units[].text` JSON을 호출자에게 반환 |
| 사용자 분석 | `collect-user-context` | 자료와 확인 가능한 공개 링크에서 사실·경험·역량을 구조화 | `src/user-info/` | `__workspace__/agent/USER_INSPECTION.md` 전체 재생성 |
| 사용자 분석 | `review-user-profile` | 프로필을 섹션별로 표시하고 사용자 승인·정정 반영 | `USER_INSPECTION.md`, `PASS`/`FIX`/`MANUAL` 응답 | 검증된 섹션을 같은 파일에 원자적으로 반영 |
| 공고 수집 | `collect-job` | URL별 공개 공고 본문을 요약 없이 정제·보존 | `src/jobs/JOB_SEEKER.md` | `__workspace__/agent/jobs/<공고명>_<수집일>.md` |
| 통합 지원 | `write-korean-cover-letter` | 프로필 구축, 현재 공고 탐색·적합도 비교, 맞춤 자기소개서 작성 | 사용자 자료·대화, 공고 또는 문항, 공개 웹 | 대화 응답으로 프로필 요약, 공고 비교표, 초안과 근거 매핑 제공 |

### 4.1 `setup-workspace`

버전 관리되는 `scripts/setup_workspace.py`를 `python3`로 실행한다. 기존 디렉터리와 `JOB_SEEKER.md`는 보존하므로 반복 실행할 수 있다. 심볼릭 링크나 기대한 파일 종류와 충돌하는 경로는 오류로 처리한다.

### 4.2 `parse-document-files`

다른 Skill을 위한 하위 수준 어댑터다. 문서 의미를 분석하거나 프로필 파일을 직접 쓰지 않는다. `python3`와 `uv`를 확인하고 `__workspace__/agent/parse-document-files-venv/`에 격리 환경을 만든다. 형식별 `scripts/parse_<format>.py`가 없으면 실제 입력에 필요한 파서를 생성·검증하는 확장 지점을 가진다. 한 파일의 실패가 다른 파일의 추출 결과를 폐기하지 않는 부분 성공 방식이다.

### 4.3 `collect-user-context`

`src/user-info/`를 재귀적으로 조사한다. 텍스트 파일은 파일명과 줄 번호를, 비텍스트 문서는 파서가 반환한 locator를 출처로 사용한다. 자료에 포함된 공개 블로그·GitHub·LinkedIn 링크는 동일성을 확인한 뒤 접근 가능한 범위에서 조사한다.

출력은 다음 세 섹션을 정해진 순서로 갖는다.

1. `사용자에 대한 객관적인 사실`
2. `사용자 역량`
3. `사용자의 경험`

경험은 중복 사건을 합친 뒤 `EXP-001` 형식의 ID를 부여한다. 역량은 직접 뒷받침하는 경험 ID만 참조한다. 상세 스키마와 누락·충돌 처리 규칙은 `references/user-inspection-format.md`가 정의한다.

### 4.4 `review-user-profile`

`USER_INSPECTION.md`를 `정보` → `역량` → `경험` 순서로 한 섹션씩 검토한다. 화면에는 읽기 쉬운 표를 표시하지만 저장 파일은 정규 Markdown 계약을 유지한다.

- `PASS`: 현재 섹션 승인
- `FIX`: 대화로 받은 정정만 반영한 뒤 같은 섹션 재검토
- `MANUAL`: 작업공간 루트의 섹션별 임시 파일을 사용자가 편집한 뒤 검증·반영

수정 때마다 세 섹션 구조, 출처, 경험 ID의 유일성, 역량에서 경험으로 향하는 참조 무결성을 전체 검사한다. 사용자 확인으로 바뀐 사실과 경험에는 별도 출처 표시를 남긴다.

### 4.5 `collect-job`

`JOB_SEEKER.md`의 Markdown 링크와 원문 URL을 등장 순서대로 읽고 fragment만 다른 중복을 포함해 같은 URL을 한 번만 처리한다. 각 공개 페이지의 최종 본문과 필요한 공개 첨부·iframe을 확인하며, 검색 snippet으로 대체하지 않는다.

출력은 공고별 원문 보존 문서다. 공고명, 선택적으로 기업명, 입력 또는 공식 대체 원문 URL, 수집일을 메타데이터로 기록하고, 모집 관련 본문은 번역·요약·재분류하지 않는다. 파일 단위 부분 성공과 원자적 교체를 적용한다. 상세 선택·파일명·본문 계약은 `references/extraction-contract.md`가 정의한다.

### 4.6 `write-korean-cover-letter`

사용자 요청에 따라 프로필 구축, 공고 탐색, 자기소개서 작성 중 필요한 단계부터 시작하는 통합 Skill이다. 현재 공고와 기업 정보를 다룰 때 공개 웹을 실제로 확인하고 링크, 공고 상태·마감일과 확인 날짜를 제시한다.

자기소개서 결과에는 초안뿐 아니라 문단별 사용자 사실·JD 요구사항의 근거 매핑, 검증할 값, 사용하지 않은 핵심 소재와 글자 수를 함께 제공한다. 문항별 작성 관점과 퇴고 기준은 `references/writing-guide.md`에 분리되어 있다.

## 5. 데이터 계약과 일관성

Skill 간 결합은 공유 파일의 경로와 Markdown/JSON 계약에 한정한다.

- 사용자 프로필 계약: `collect-user-context/references/user-inspection-format.md`
- 프로필 표시·수동 편집 계약: `review-user-profile/references/review-format.md`
- 채용공고 원문 계약: `collect-job/references/extraction-contract.md`
- 문서 추출 반환 계약: `parse-document-files/SKILL.md`의 JSON 구조

파일을 생성하거나 수정하는 Skill은 가능한 경우 완성본을 같은 디렉터리의 임시 파일에 먼저 기록한 뒤 최종 경로로 원자적으로 교체한다. 필수 입력이 없거나 계약을 안전하게 검증할 수 없으면 기존 산출물을 유지한다. 수집은 현재 입력을 기준으로 전체 재생성하며 과거 결과와 암묵적으로 병합하지 않는다.

## 6. 보안과 출처 정책

모든 Skill에 공통으로 다음 경계를 적용한다.

- 사용자 자료나 공개 원문에 없는 사실·경험·수치·요건을 만들지 않는다.
- 핵심 사용자 사실과 경험에는 파일 위치, 문서 locator, 공개 URL 또는 사용자 확인 출처를 남긴다.
- 주민등록번호, 상세 주소, 금융정보, 비밀번호, API 키·secret·token 등 불필요하거나 인증에 쓰이는 민감정보를 수집·복제·저장하지 않는다.
- 나이·성별·사진·가족관계 등 차별 가능 정보는 명시적 필요가 있을 때만 사용하며 적합도 판단에는 반영하지 않는다.
- 로그인, CAPTCHA, `robots.txt`, 이용약관과 접근 제한을 우회하지 않는다.
- 공개 공고는 원문 페이지를 확인하고 공고 상태·마감일·확인 날짜를 구분한다. 출처에서 확인된 사실과 모델의 해석을 분리한다.
- 사용자 입력 경로 밖을 가리키는 심볼릭 링크를 따라가지 않는다.

## 7. 외부 의존성과 확장 지점

- Python 3: 작업공간 초기화 스크립트와 문서 파서 실행에 사용한다.
- `uv`: 문서 형식별 라이브러리를 작업공간 내부 가상환경에 격리해 설치한다.
- 웹 접근: 공개 프로필·채용공고·기업 정보의 수집과 최신성 검증에 사용한다.
- 문서 형식별 파서: `parse-document-files/scripts/parse_<format>.py`로 추가할 수 있다. 현재 배포물에는 형식별 파서가 미리 포함되어 있지 않다.

새 기능은 최종 사용자가 직접 실행해야 하면 `call-my-name/skills/` 아래에 Skill로 추가한다. 핵심 운영 규칙은 `SKILL.md`, 큰 형식 계약과 가이드는 `references/`, 반복 가능하고 결정적인 처리는 `scripts/`에 둔다.

## 8. 현재 구현 경계

현재 플러그인에는 별도 MCP 서버, App, Hook 또는 데이터베이스가 포함되어 있지 않다. 외부 정보 접근은 Codex 실행 환경이 제공하는 웹 기능을 사용하며, 프로필과 수집 공고는 사용자 작업공간의 Markdown 파일로 보존한다.

또한 `write-korean-cover-letter`는 구성 가능한 수집 Skill의 산출물을 반드시 입력으로 소비하도록 강제된 오케스트레이터가 아니라 독립적인 통합 Skill이다. 따라서 현재 아키텍처에서 자동화된 종단 간 파이프라인은 Skill 선택과 파일 계약을 따르는 Codex의 실행 흐름으로 구성된다.
