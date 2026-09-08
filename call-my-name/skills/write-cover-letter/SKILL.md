---
name: write-cover-letter
description: Write one or more truthful Korean cover-letter answers from questions supplied in the prompt or a referenced file, using the candidate context created by the previous call-my-name workflow. Optionally tailor answers to a user-supplied Job Description. Create one target file per question through one subagent per answer. Use when the user asks to 자기소개서 작성, 자소서 문항 답변, cover letter answers, 문항별 초안, or a 글자 수 제한 자기소개서.
---

# 자기소개서 문항 작성

사용자가 제공한 자기소개서 문항마다 정해진 글자 수 이내의 한국어 초안을 작성하고, 작업별 `target/` 하위 디렉터리에 문항별 Markdown 파일을 남긴다.

## 입력 확인

1. 사용자 프롬프트에서 문항을 읽는다. 파일 레퍼런스가 제공되면 해당 파일을 읽어 문항을 추출한다. 둘 다 있으면 중복 문항을 제거하고 해석이 필요한 부분만 확인한다.
2. 문항마다 글자 수 제한을 확인한다. `700자`, `(700자)`, `700자 이내`처럼 문항에 붙은 단일 숫자 표기는 모두 해당 문항의 최대 글자 수로 해석한다. 그 밖에 여러 해석이 가능하거나 제한이 없으면 작성 전에 확인한다. 사용자가 명시적으로 제한이 없다고 답하면 보수적인 초안으로 작성하고 실제 글자 수를 표시한다.
3. 사용자 컨텍스트 선행 워크플로우는 반드시 `$collect-user-context` → `$review-user-profile` 순서로 완료되어야 한다. `$collect-user-context`가 실행 작업공간 루트의 `__workspace__/agent/USER_INSPECTION.md`를 생성하고, `$review-user-profile`이 사용자 승인·정정을 반영해 같은 파일을 갱신하므로, 자기소개서 작성에는 이 최종 공유 파일만 사용자 컨텍스트 분석 자료로 사용한다.
4. `__workspace__/agent/USER_INSPECTION.md`가 없거나, `사용자에 대한 객관적인 사실` → `사용자 역량` → `사용자의 경험`의 필수 섹션을 안전하게 읽을 수 없으면 Skill을 실행하지 마라. 답변용 Subagent, `target/` 작업 디렉터리 또는 답변 파일을 만들거나 바꾸지 말고, 사용자에게 "선행 사용자 컨텍스트 분석 자료가 없어 사실에 근거한 자기소개서를 작성할 수 없다"는 사유와 함께 `$collect-user-context`를 먼저 실행한 뒤 `$review-user-profile`로 검토를 완료해야 한다고 안내하라. 이 Skill이 두 선행 Skill을 대신 호출하지 마라.
5. 사용자가 프롬프트 또는 파일로 Job Description을 제공한 경우에만 그 요구 역량·업무를 반영한다. 제공하지 않은 회사·공고·직무 정보는 추정하거나 웹에서 보완하지 않는다.
6. 답변 파일을 만들기 전에 문항별 핵심 입력을 판정한다. 지원 동기·회사 선택 이유처럼 지원 회사를 직접 묻는 문항에는 확인 가능한 지원 회사 정보가, 지원 직무 선택 이유·희망 업무·직무 적합성처럼 목표 직무를 직접 묻는 문항에는 지원 직무 정보가 필요하다. 사용자 컨텍스트의 현재/과거 회사·직무는 지원 대상이라고 명시되지 않은 한 이를 대신하지 않는다.
7. 필요한 회사 또는 지원 직무가 빠졌다면, 아직 `target/` 결과 디렉터리나 답변 파일을 만들지 말고 누락된 항목만 한 번에 질문한다. 회사 선택 이유를 묻는 경우에는 회사명만으로 검증 가능한 이유를 만들 수 없으므로, 사용자가 제시할 회사 관련 사실·가치 또는 본인의 지원 이유도 함께 요청한다. Job Description은 이 확인을 보완할 수 있지만 선택 입력이며, 제공하지 않았다는 이유만으로 질문하지 않는다. 정보를 받은 뒤에만 해당 문항들을 다시 사전 점검한다.

## 제외 범위와 사실성

- `$collect-job`을 호출하지 말고, `src/jobs/`, `__workspace__/agent/jobs/` 및 외부 모집공고 수집 Skill의 결과를 읽거나 사용하지 마라.
- 사용자 컨텍스트와 사용자가 제공한 Job Description 외의 모집공고 정보는 고려하지 마라.
- `USER_INSPECTION.md`의 사실·경험·역량 및 사용자가 현재 대화에서 확인한 정보만 사용한다. 경험, 수치, 역할, 성과, 회사 정보, 동기를 창작하지 마라.
- 주민등록번호, 상세 주소, 계정·인증 정보 등 불필요한 개인정보를 답변이나 파일에 넣지 마라.

## 문항별 병렬 작성과 저장

상세 파일 형식과 품질 기준은 [references/output-contract.md](references/output-contract.md)를 읽어 적용한다.

1. 모든 문항의 사전 입력 점검을 통과한 뒤에만 현재 실행 작업공간 루트의 `target/` 안에 이번 작업만 위한 새 디렉터리 `cover-letter-YYYYMMDD-HHMMSS/`를 생성한다. 같은 이름이 있으면 안전한 짧은 순번을 붙이며, 기존 작업 디렉터리와 파일은 덮어쓰지 마라.
2. 문항마다 정확히 하나의 Subagent를 만든다. 각 Subagent에게 해당 문항, 글자 수 제한, 선택적 Job Description, `USER_INSPECTION.md`의 관련 사실·경험만 전달한다. 서로 다른 Subagent가 같은 문항이나 같은 출력 파일을 맡지 않게 한다.
3. 각 Subagent는 자신에게 배정된 `target/cover-letter-.../question-XX.md` 하나를 직접 작성한다. 상위 Agent가 답변 본문을 대신 파일에 쓰거나, 다른 Agent가 그 파일을 작성하게 해서는 안 된다. 계약 실패 시에도 같은 담당 Subagent에게만 수정 요청한다.
4. Subagent는 문항에 직접 답하고 제한 이내인지 확인한 완성본만 파일에 기록한다. 다른 문항의 파일을 읽거나 수정하지 않는다.
5. 모든 Subagent 완료 뒤 상위 Agent는 파일별 문항 대응, UTF-8, 글자 수 제한, 사실 근거, 파일 경로를 검사한다. `확인 필요`, 미확인 회사·지원 직무, 또는 문항의 핵심에 답하지 않는 표현이 있으면 완성본으로 취급하지 않고 같은 담당 Subagent에게만 수정 요청하거나 사용자에게 최소 정보를 재확인한다.
6. 검증 실행에서는 [references/verification-evidence.md](references/verification-evidence.md)의 비밀정보 없는 원본 증거 보존 절차를 따른다. 보고서의 표나 사후 서술로 원본 위임·직접 작성·금지 경로 미사용 증거를 대체하지 않는다.

## 사용자에게 제공할 결과

- 생성 디렉터리와 문항별 파일 경로를 나열한다.
- 각 파일의 글자 수 기준(공백 포함/제외)과 측정값, 반영한 선택적 Job Description 여부를 짧게 표시한다.
- 사용자 컨텍스트에서 확인이 필요한 사실이나 제한을 충족하기 위해 생략한 내용을 별도로 알린다.
- 모든 파일이 준비되기 전에는 일부 결과를 완료로 표현하지 마라.
