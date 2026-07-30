---
name: parse-document-files
description: Parse and extract source-located text from non-plain-text document files such as PDF, DOCX, XLSX, and PPTX for other call-my-name skills. Use when a caller needs readable document content with page, paragraph, slide, sheet, or row locators. Return extracted units without interpreting candidate facts, analyzing content, or writing downstream profile files.
---

# 문서 파일 파싱

PDF, DOCX, XLSX, PPTX 등 원문 그대로 읽을 수 없는 문서에서 의미 있는 텍스트와 출처 위치를 추출해 호출한 Skill에 반환하라. 문서 내용의 의미를 분석하거나 사용자 정보를 구조화하지 마라.

## 입력과 책임

- 호출한 Skill이 지정한 파일만 처리하고 각 파일의 정확한 경로를 입력으로 사용하라.
- 일반 파일인지 확인하고, 호출자가 지정한 범위 밖을 가리키는 심볼릭 링크는 따라가지 마라.
- 이 Skill이 설치된 디렉터리를 `SKILL_DIR`, 실행 작업공간의 루트를 `WORKSPACE_ROOT`로 지칭하라.
- 파일마다 독립적으로 처리하여 한 파일의 실패 때문에 다른 파일의 결과를 버리지 마라.

## 실행 환경

1. 파서를 만들거나 실행하기 전에 `python3 --version`과 `uv --version`을 각각 확인하라.
2. 둘 중 하나라도 설치되어 있지 않거나 실행되지 않으면 설치를 대신 시도하지 말고 문서 처리를 중단하라.
   - `설치되지 않음: python3`, `설치되지 않음: uv`처럼 누락되거나 실행할 수 없는 프로그램을 각각 명시하라.
   - 현재 운영체제와 패키지 관리자를 확인할 수 있으면 프로그램별 실제 설치 명령, 명령 실행 뒤 필요한 셸 재시작이나 `PATH` 적용 방법, 설치 확인 명령을 순서대로 설명하라. 공식 설치 문서는 보조 링크로 함께 제공할 수 있지만 URL만 단독으로 제시하지 마라.
   - 운영체제나 패키지 관리자를 확정할 수 없으면 임의의 설치 명령을 제시하지 말고 Python은 `https://www.python.org/downloads/`, uv는 `https://docs.astral.sh/uv/getting-started/installation/`을 안내하라.
   - 설치 후 `python3 --version`과 `uv --version`을 모두 다시 실행해 달라고 요청하라.
3. `WORKSPACE_ROOT/__workspace__/agent/parse-document-files-venv/`를 `uv venv --python python3`로 생성하고 이후 실행에서 재사용하라.
4. 파서에 필요한 패키지는 `uv pip install --python <venv-python> ...`으로 이 환경에만 설치하고 전역 Python 환경을 변경하지 마라.

## 형식별 파서

1. 파일 형식마다 `SKILL_DIR/scripts/parse_<format>.py` 형식의 전용 Python 파서가 있는지 확인하라. 하나의 파서는 하나의 파일 형식만 처리해야 한다.
2. 파서가 없으면 해당 형식과 공개 명세에 맞는 파서를 작성하라. 초기 배포물에 파서나 패키지 목록이 있다고 가정하지 말고 실제 입력 형식에 필요한 코드와 라이브러리만 선택하라.
3. 새 파서는 실제 입력을 처리하기 전에 최소 입력 또는 안전한 합성 파일로 실행 가능성을 검사하라.
4. 파서의 stdout은 결과 JSON만 출력하고 진단은 stderr에 쓰며 실패 시 0이 아닌 종료 코드를 반환하게 하라.

## 반환 계약

파일별 결과를 다음 JSON 계약으로 호출한 Skill에 반환하라.

```json
{
  "source_file": "파일명",
  "units": [
    {"locator": "page 1 | paragraph 3 | slide 2 | sheet 성적 row 4", "text": "추출 본문"}
  ]
}
```

- `source_file`에는 호출자가 결과를 원본과 연결할 수 있는 파일명을 기록하라.
- `units`에는 본문, 표 셀, 하이퍼링크 표시 문자열처럼 의미 있는 내용만 원문 순서대로 기록하라.
- `locator`는 파일 형식에 맞는 페이지, 문단, 슬라이드, 시트·행 등의 위치를 식별할 수 있어야 한다.
- 문서 작성자, 생성 프로그램, 생성·수정 시각 등 파일 메타데이터는 출력하지 마라.
- 내용을 추출할 수 없는 파일은 빈 `units`를 정상 결과처럼 반환하지 말고 접근 불가 사유를 호출한 Skill에 명시하라.

## 실패 처리

- 스캔 문서처럼 텍스트를 추출할 수 없거나, 패키지를 설치할 수 없거나, `SKILL_DIR/scripts/`에 쓸 수 없으면 해당 파일을 접근 불가로 기록하고 내용을 추측하지 마라.
- 지원하지 않는 형식을 다른 형식으로 가장해 처리하지 마라.
- 처리 가능한 파일의 결과는 유지하고, 접근 불가 파일과 그 사유를 호출한 Skill에 함께 반환하라.
- 이 Skill은 추출 결과를 해석하거나 `USER_INSPECTION.md` 같은 후속 산출물을 만들거나 변경하지 마라.
