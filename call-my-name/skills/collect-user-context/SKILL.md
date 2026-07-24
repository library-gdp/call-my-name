---
name: collect-user-context
description: Read, collect, inspect, parse, extract, inventory, organize, summarize, and structure a job seeker's personal facts, career history, education, research, certifications, links, resumes, portfolios, career descriptions, and prior cover letters from files placed in workspace-root src/. Infer evidence-backed capabilities and map them to deduplicated experiences, then write USER_INSPECTION.md for downstream job matching and application writing. Use aggressively when the user asks to 내 정보·이력·경력·학력·경험·역량을 수집, 불러오기, 읽기, 파싱, 분석, 추출, 정리, 구조화, 프로필화, 인벤토리화하거나 지원자 컨텍스트·후보자 프로필·이력 자료 분석을 요청할 때, and whenever files or public profile/blog/GitHub links should become reusable candidate context. Trigger for text, PDF, DOCX, PPTX, XLSX, resumes, CVs, transcripts, portfolios, career documents, and cover-letter archives. Do not use for job-posting discovery or application drafting unless collecting the user's source context is part of that request.
---

# 사용자 컨텍스트 수집

사용자가 제공한 자료에서 확인되는 사실, 경험, 역량만 구조화하라. 결과는 후속 Agent가 읽는 내부 계약이므로 간결하되 출처와 경험 참조를 보존하라.

## 경로 확정

- 실행 작업공간의 루트를 기준으로 입력은 `src/`, 출력은 `__workspace__/agent/USER_INSPECTION.md`로 고정하라.
- 이 Skill이 설치된 디렉터리는 `SKILL_DIR`로 지칭하라. 동적으로 만든 파서는 `SKILL_DIR/scripts/` 아래에만 두라.
- `src/` 아래의 일반 파일을 재귀적으로 조사하되 `src/` 밖을 가리키는 심볼릭 링크는 따라가지 마라.
- `src/`가 없거나, 파일이 없거나, 모든 파일에서 사용자와 관련된 사실을 하나도 확인하지 못하면 출력 파일을 만들거나 바꾸지 마라. 작업을 즉시 끝내고 사용자에게 작업공간의 `src/`에 이력서, 경력기술서, 포트폴리오 등 적절한 자료를 넣어 달라고 요청하라.

## 자료 읽기

1. 읽을 수 있는 텍스트 파일은 원문 그대로 읽고 파일명과 줄 번호를 출처 위치로 기록하라.
2. 바이너리 파일마다 `SKILL_DIR/scripts/parse_<format>.py` 형식의 전용 Python 파서가 있는지 확인하라. 하나의 파서는 하나의 파일 형식만 처리해야 한다.
3. 파서가 없으면 해당 형식과 공개 명세에 맞는 파서를 먼저 작성하라. 초기 배포물에 파서나 패키지 목록이 있다고 가정하지 말고, 실제 입력 형식에 필요한 코드와 라이브러리만 선택하라.
4. 파서를 만들거나 실행하기 전에 `python3 --version`과 `uv --version`을 각각 확인하라. 둘 중 하나라도 설치되어 있지 않거나 실행되지 않으면 설치를 대신 시도하지 말고 바이너리 문서 처리를 중단하라.
   - `설치되지 않음: python3`, `설치되지 않음: uv`처럼 누락되거나 실행할 수 없는 프로그램을 각각 명시하라.
   - 현재 운영체제와 패키지 관리자를 확인할 수 있으면 프로그램별 실제 설치 명령, 명령 실행 뒤 필요한 셸 재시작이나 `PATH` 적용 방법, 설치 확인 명령을 순서대로 설명하라. 공식 설치 문서는 보조 링크로 함께 제공할 수 있지만 URL만 단독으로 제시하지 마라.
   - 운영체제나 패키지 관리자를 확정할 수 없으면 임의의 설치 명령을 제시하지 말고 Python은 `https://www.python.org/downloads/`, uv는 `https://docs.astral.sh/uv/getting-started/installation/`을 안내하라.
   - 설치 후 `python3 --version`과 `uv --version`을 모두 다시 실행해 달라고 요청하라.
5. `<workspace>/__workspace__/agent/collect-user-context-venv/`를 `uv venv --python python3`로 생성하고 이후 실행에서 재사용하라. 파서에 필요한 패키지는 `uv pip install --python <venv-python> ...`으로 이 환경에만 설치하라. 전역 Python 환경을 변경하지 마라.
6. 새 파서는 실제 입력을 처리하기 전에 최소 입력 또는 안전한 합성 파일로 실행 가능성을 검사하라. 파서의 stdout은 아래 JSON 계약을 따르고 진단은 stderr에 쓰며 실패 시 0이 아닌 종료 코드를 반환하게 하라.

```json
{
  "source_file": "파일명",
  "units": [
    {"locator": "page 1 | paragraph 3 | slide 2 | sheet 성적 row 4", "text": "추출 본문"}
  ]
}
```

- 본문, 표 셀, 하이퍼링크 표시 문자열처럼 의미 있는 내용만 추출하라. 문서 작성자, 생성 프로그램, 생성·수정 시각 등 파일 메타데이터는 출력하지 마라.
- 스캔 문서처럼 텍스트를 추출할 수 없거나, 패키지를 설치할 수 없거나, `SKILL_DIR/scripts/`에 쓸 수 없는 파일은 접근 불가로 기록하고 그 파일에서 정보를 추측하지 마라.
- 접근 불가 자료는 무시하고 나머지 자료로 계속하라. 처리 가능한 관련 자료가 하나도 남지 않으면 `src/`에 읽을 수 있는 자료를 제공해 달라고 요청하고 종료하라.

## 정보와 공개 링크 수집

- 제공된 항목만 수집하라: 이름, 생년월일 또는 나이, 전화번호, 이메일, 경력의 회사·기간·고용 형태·소속·직책·직무·업무·프로젝트·성과·기술·재직 상태, 학력의 학교·학위 종류·전공·기간·학적 상태·소재지·학점·평점·과목별 성적과 그 밖의 학업 정보, 연구·논문·연구실·담당교수, 자격증, 어학, 프로젝트, 아르바이트, 자기소개서·포트폴리오·이력서·경력기술서의 경험, 블로그·GitHub·LinkedIn 등 관련 링크.
- 값이 없으면 원칙적으로 항목 자체를 생략하되, 출력 계약이 학력·경력의 필수 필드에 `자료에서 확인되지 않음`을 요구하면 그 표기를 따르라. 날짜, 수치, 역할, 문제, 해결 과정, 결과, 느낀점을 보완하거나 창작하지 마라. 성적 환산은 원자료에 환산값이나 환산 기준이 있을 때만 기록하라.
- 링크가 있으면 공개 웹을 실제로 열어 확인하라. 계정·작성자 동일성을 자료의 링크와 공개 프로필로 확인한 뒤, 작성물 목록의 페이지네이션이 끝날 때까지 공개 블로그 글과 공개 GitHub 활동·저장소·기여를 수집하라. 각 항목에 원문 URL을 남겨라.
- 로그인, CAPTCHA, robots.txt, 이용약관 또는 접근 제한을 우회하지 마라. 비공개·삭제·차단 콘텐츠는 접근 불가로 보고 무시하라.
- 사용자와 무관한 정보는 제외하라. 관련 여부를 합리적으로 확정할 수 없는 정보는 포함하되 `[관련성 확인 필요]`를 붙여라.
- 주민등록번호, 여권·운전면허 식별번호, 상세 주소, 금융 계정·비밀번호, 계정 비밀번호, API 키·secret·token 등 인증정보는 수집·복사·출력하지 마라. 전화번호와 이메일은 사용자가 제공한 연락처로 확인될 때만 허용하라.

## 사실, 경험, 역량 구성

출력하기 전에 [references/user-inspection-format.md](references/user-inspection-format.md)를 읽고 그 계약을 적용하라.

1. 가치판단 없이 확인되는 인적·경력·학력·연구·자격·링크 사실을 정리하라.
2. 학력은 학교별로, 경력은 근무 회사별로 하나의 항목을 만들고 각 항목의 속성을 하위 목록으로 묶어라. 학교명과 전공을 서로 독립된 학력 항목으로 만들거나, 회사와 그 회사에서 수행한 프로젝트를 서로 독립된 경력 항목으로 만들지 마라.
3. 회사에서 수행한 업무·프로젝트·성과·사용 기술은 해당 회사의 경력 항목 아래에 귀속하라. 동일 회사에 재입사했거나 고용 관계가 명확히 분리된 경우에만 별도 경력 항목으로 나눠라.
4. 모든 경험 후보를 모아 같은 사건은 하나로 합치고 `EXP-001`부터 안정적인 순서로 번호를 부여하라.
5. 각 경험에는 객관적 사실을 반드시 포함하라. 문제, 해결 방식·과정, 느낀점은 원자료에 명시된 경우에만 포함하라.
6. 원자료의 반복된 행동, 역할, 결과가 직접 뒷받침하는 역량만 작성하라. 새 역량을 창작하거나 숙련도를 추측하지 마라.
7. 각 역량의 근거는 설명을 복제하지 말고 `EXP-*` ID로만 연결하라. 존재하지 않는 경험 ID를 참조하지 마라.
8. 핵심 사실과 각 경험에는 `[출처: <파일명>#<locator>]` 또는 `[출처: <URL>]`을 붙여 후속 Agent가 검증할 수 있게 하라.

## 결과 저장

- 세 섹션을 모두 구성한 뒤에만 `__workspace__/agent/`를 생성하라.
- 임시 파일에 완성본을 쓴 뒤 `USER_INSPECTION.md`로 원자적으로 교체하라. 기존 결과와 병합하지 말고 현재 `src/`와 현재 접근 가능한 공개 링크만으로 전체를 재생성하라.
- 완료 전에 민감정보 제외, 중복 경험 통합, 출처 존재, `EXP-*` 참조 무결성, 미제공 내용의 비창작 여부를 검사하라.
