---
name: collect-job
description: Read recruitment-posting URLs from workspace-root src/jobs/JOB_SEEKER.md, visit each public posting, extract only the source wording that belongs or may relate to the opening without summarizing or rewriting it, and save one cleaned Markdown file per posting under __workspace__/agent/jobs/. Use when the user has collected 채용공고·모집공고 URLs in JOB_SEEKER.md and asks to 가져오기, 수집, 불러오기, 추출, 원문화, 저장, 동기화, or prepare the postings for downstream review.
---

# 채용공고 수집

`src/jobs/JOB_SEEKER.md`에 모인 공개 URL을 따라가 채용공고 본문을 원문 표현 그대로 추출하고, 공고별 Markdown 파일로 저장하라.

## 입력과 출력 경로

- 실행 작업공간의 루트를 기준으로 입력을 `src/jobs/JOB_SEEKER.md`, 출력 디렉터리를 `__workspace__/agent/jobs/`로 고정하라.
- 입력 파일이 없거나 URL이 하나도 없으면 출력 파일을 만들거나 바꾸지 말고, 필요한 파일과 경로를 사용자에게 안내하라.
- Markdown 링크와 `http://` 또는 `https://` 원문 URL을 등장 순서대로 읽고, 같은 URL의 중복과 URL fragment만 다른 중복은 한 번만 처리하라.
- URL이 아닌 입력 내용은 공고 본문으로 간주하지 마라.

## 수집 절차

수집 전에 [references/extraction-contract.md](references/extraction-contract.md)를 끝까지 읽고 선택·보존·파일명·출력 계약을 적용하라.

1. 각 URL의 공개 페이지를 실제로 열고 redirect된 최종 페이지를 확인하라. 검색 결과의 snippet만으로 공고를 만들지 마라.
2. JavaScript 실행 안내나 빈 HTML shell만 보이면 즉시 실패 처리하지 마라. 사용 가능한 브라우저 렌더링을 먼저 시도하고, HTML의 JSON-LD·초기 상태 데이터와 페이지가 인증 없이 호출하는 공개 데이터 요청을 확인하라. 비공개 API를 추측하거나 자격 증명이 필요한 요청을 호출하지 마라.
3. 공고 본문이 공개 iframe, 이미지, PDF 또는 첨부 문서에 있으면 해당 자료까지 확인하라. 다른 공고나 사이트 일반 정보로 이어지는 링크는 따라가지 마라.
4. 모집공고에 직접 관련된 내용과 간접적으로 유용한 내용을 선택하라. 관련 여부가 애매하면 포함하라.
5. 선택한 내용의 문구, 수치, 항목 관계와 등장 순서를 보존하라. 요약, 해석, 번역, 교정, 재분류 또는 누락값 보완을 하지 마라.
6. HTML·CSS·JavaScript, 페이지 공통 UI와 공고에 무관한 지표·홍보 문구를 제거하라. 표현을 Markdown으로 옮기는 데 필요한 최소한의 제목·목록·표 구조만 사용하라.
7. 공고별 결과를 완성한 뒤 `__workspace__/agent/jobs/`를 만들고, 임시 파일을 거쳐 최종 파일로 원자적으로 교체하라.
8. 위 공개 경로를 모두 확인해도 본문을 신뢰할 수 없을 때만 파일을 만들지 말고 이유를 기록한 뒤 나머지 URL을 계속 처리하라.

로그인, CAPTCHA, `robots.txt`, 이용약관 또는 그 밖의 접근 제한을 우회하지 마라. 원 URL이 차단되면 그 페이지가 직접 가리키는 공개 회사 채용 페이지나 공개 첨부 문서만 대체 원문으로 사용할 수 있다. 추측이나 검색 snippet으로 대체하지 마라.

## 완료 점검

- 성공한 공고마다 계약에 맞는 파일이 하나씩 존재하는지 확인하라.
- 원문 URL과 수집일이 정확하며, 파일명에 약식 공고명과 수집일이 포함되는지 확인하라.
- 출처에 있는 관련 항목을 빠뜨리거나 원문을 요약·재작성하지 않았는지 확인하라.
- 사이트 공통 요소, 코드, 조회수·즐겨찾기 등 무관한 내용이 남지 않았는지 확인하라.
- 없는 날짜, 경력, 자격, 급여나 절차를 만들지 않았는지 확인하라.
- 완료 보고에는 성공한 파일 경로와 실패한 URL별 사유만 간결하게 제시하라.
