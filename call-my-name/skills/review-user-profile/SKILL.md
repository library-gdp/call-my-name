---
name: review-user-profile
description: Review, approve, and revise the facts, capabilities, and experiences in __workspace__/agent/USER_INSPECTION.md produced by collect-user-context. Present each section as a readable table and collect PASS, FIX, or MANUAL feedback one section at a time. Use when the user asks to review, verify, correct, approve, or manually edit a collected candidate profile, 사용자 정보·역량·경험 검토, 프로필 정정, 사용자 확인, or USER_INSPECTION.md review.
---

# 사용자 프로필 검토

`collect-user-context`가 만든 사용자 프로필을 `정보` → `역량` → `경험` 순서로 검토하고 사용자의 정정과 승인을 반영하라.

## 입력 확인

- 먼저 사용자의 실행 작업공간 루트를 `WORKSPACE_ROOT`로 확정하라. 입력과 출력은 정확히 `WORKSPACE_ROOT/__workspace__/agent/USER_INSPECTION.md`로 고정하라. Skill 디렉터리나 `WORKSPACE_ROOT/agent/USER_INSPECTION.md`를 대신 사용하지 마라.
- 작업을 시작하기 전에 `../collect-user-context/references/user-inspection-format.md`와 [references/review-format.md](references/review-format.md)를 읽어라.
- 파일이 없거나, 세 개의 필수 2단계 제목이 정해진 순서로 없거나, 내용을 안전하게 파싱할 수 없으면 파일을 만들거나 바꾸지 마라. `$collect-user-context`로 프로필을 먼저 생성하거나 복구해 달라고 안내하고 종료하라.
- 주민등록번호, 상세 주소, 금융정보, 비밀번호, API 키·secret·token 등 금지된 민감정보를 새로 저장하지 마라. 발견하면 값은 복제하지 말고 사용자에게 제거가 필요하다고 알려라.

## 섹션별 검토

한 번에 하나의 섹션만 처리하라. 사용자에게는 각각 `정보`, `역량`, `경험`이라는 이름으로 보여주고, 원본 Markdown 대신 `review-format.md`의 표를 제시하라.

각 표 뒤에서 `PASS`, `FIX`, `MANUAL` 중 하나의 응답을 받아라. 선택형 사용자 입력 기능을 사용할 수 있으면 세 응답을 명시적인 선택지로 제공하라.

1. `PASS`: 현재 섹션을 바꾸지 말고 다음 섹션으로 이동하라.
2. `FIX`: 고칠 내용을 자유 형식으로 입력해 달라고 요청하라. 사용자 설명으로 확인되는 변경만 현재 섹션에 적용하고, 형식과 문서 전체 참조 무결성을 검사한 뒤 파일을 원자적으로 교체하라. 수정된 같은 섹션을 표로 다시 보여주고 응답을 기다려라.
3. `MANUAL`: `review-format.md`에 정한 파일을 작업공간 루트에 만들고 사용자가 직접 수정하게 하라. 사용자가 `완료`라고 입력하면 파일을 다시 읽어 검증하고 해당 섹션만 원자적으로 교체하라. 성공적으로 반영한 뒤에만 수동 파일을 삭제하고, 수정된 같은 섹션을 표로 다시 보여주고 응답을 기다려라.

세 섹션이 모두 `PASS`를 받으면 검토 완료를 알리고 최종 파일 경로를 제시하라.

## 수정과 무결성

- 사용자가 정정한 사실에는 `[출처: 사용자 확인]`을 붙여라. 사용자가 정정한 경험의 출처 목록에는 `사용자 확인`을 추가하라.
- 원출처가 여전히 뒷받침하는 내용은 유지하되 정정 내용과 충돌하는 출처는 제거하라. 사용자가 말하지 않은 사실, 문제, 해결 과정, 느낀점은 만들지 마라.
- 역량이 수정되면 현재 `사용자의 경험` 전체에서 직접 근거가 되는 경험을 다시 찾아 `EXP-*` ID로 매핑하라. 단어가 비슷하다는 이유만으로 추측해 연결하지 마라. 근거를 찾지 못한 사용자 확인 역량은 `근거 경험` 블록 없이 유지하라.
- 경험 수정으로 ID가 추가·변경·삭제되면 모든 역량 참조를 다시 검사하라. 존재하지 않는 ID는 제거하고, 명백한 근거가 있을 때만 새 ID로 다시 연결하라.
- 경험 ID는 문서에서 유일해야 한다. 기존 사건의 ID는 가능한 한 유지하고, 새 경험은 현재 최댓값 다음 번호를 사용하라.
- 각 성공적인 수정 직후 전체 문서의 세 섹션, 필수 경험 필드, 출처, `EXP-*` 참조를 검사하라. 검증에 실패하면 원본 파일을 유지하고 문제와 필요한 수정만 설명하라.

## 파일 안전

- 완성한 전체 문서를 `WORKSPACE_ROOT/__workspace__/agent/`의 임시 파일에 쓴 뒤 같은 디렉터리의 `USER_INSPECTION.md`로 원자적으로 교체하라.
- 수동 편집 파일이 이미 있으면 덮어쓰지 말고 중단된 검토의 초안으로 재사용하라.
- 수동 편집 파일에는 개인정보가 포함될 수 있으므로 SCM에 추가하지 말라고 사용자에게 알리고, 반영 전에는 삭제하지 마라.
- 검토가 중단되면 아직 반영되지 않은 수동 파일은 복구를 위해 그대로 두어라.
