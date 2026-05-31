# 대시보드 디자인 시스템

Dashboard stage와 모든 시각화에 공통 적용됩니다.
대시보드는 보고서 장식물이 아니라, 분석가가 의사결정과 근거를 함께 보여주는 작업 화면입니다.

## 레이아웃 계약
- 상단 작업바: `.workspace-header` — 데이터 파일, run ID, 산출물 상태를 표시합니다.
- 핵심 요약: `.topbar` — 왼쪽은 핵심 질문과 최종 판단, 오른쪽은 검증 상태입니다.
- 탭 구조: `Overview`, `Drivers`, `Scenario`, `Evidence`
  - `Overview`: KPI 3~5개, 메인 차트, 스토리 라인
  - `Drivers`: 원인, 세그먼트, 우선순위
  - `Scenario`: what-if가 있을 때만 유지하고, 없으면 탭과 섹션을 제거합니다.
  - `Evidence`: `04_metrics.json`, `05_analysis.py`, `05_analysis.ipynb`, 데이터 품질, 검증 예정 상태를 표시합니다. `08_validation_report.md`가 이미 있으면 요약합니다.
- 콘텐츠는 General → Specific 순서로 배치합니다.
- 페이지 섹션을 떠 있는 큰 카드처럼 중첩하지 않습니다. 카드형 UI는 KPI, 차트, 표, 검증 항목에만 사용합니다.

## 색상
- 배경: `#eef2f7`
- 기본 표면: `#ffffff`
- 보조 표면: `#f9fafb`
- 상단 작업바: `#111827`
- 본문 텍스트: `#111827`
- 보조 텍스트: `#667085`
- 경계선: `#cfd8e3`
- 정보/기준: `#1d4ed8`
- 좋음/긍정: `#16a36d`
- 나쁨/위험: `#d92d4c`
- 경고/보통: `#d98319`
- KPI 수치: `#0a0a0a` 검정 고정 — **수치에 색상 절대 금지**

## 컴포넌트
- 카드 radius는 `8px` 이하로 유지합니다.
- 탭은 segmented control처럼 보이게 만들고, active 탭만 진한 배경을 사용합니다.
- 위험/좋음/주의는 `.dot`, `.chip`, `.badge`로 표시합니다.
- KPI 카드에는 다음 정보를 포함합니다.
  - KPI 이름
  - 값
  - 계산 기준 또는 표본
  - baseline/segment/unit
  - 상태 chip
- 검증 상태 패널에는 최소 `metrics.json`, `analysis.py`, `analysis.ipynb`, 데이터 품질, run ID를 표시합니다.

## 차트
- 순수 SVG/Canvas만 사용합니다. CDN 라이브러리(Chart.js, D3, Plotly 등)는 금지합니다.
- SVG는 `width:100%; height:auto; max-height:none`으로 카드 너비에 맞춥니다.
- SVG viewBox 내부 여백: 상하 `10px`, 좌우는 축 레이블이 있으면 `40~70px`, 없으면 `8px`를 기준으로 합니다.
- 차트 플롯 영역은 viewBox 면적의 80% 이상을 사용합니다.
- 축 레이블과 범례는 viewBox 안에서 잘리지 않아야 합니다.
- 바 차트 스케일은 실제 표시값의 최대값 기준으로 잡고, 평균선/목표선 같은 기준선으로 `maxValue`를 대체하지 않습니다.
- 수직 바 차트 공식: `y = plotTop + (1 - value / maxValue) * chartHeight`, `height = (value / maxValue) * chartHeight`
- SVG 좌표 검증 필수: `<rect>`의 `x`, `y`, `width`, `height`는 모두 0 이상이어야 하며, 막대와 레이블이 viewBox 밖으로 나가면 안 됩니다.

## 타이포그래피
- 외부 폰트를 불러오지 않습니다. 시스템 폰트 스택을 사용합니다.
- 한글 텍스트는 `word-break: keep-all`을 기본으로 하고, 표와 좁은 칸은 `overflow-wrap: anywhere`를 허용합니다.
- viewport width로 폰트 크기를 스케일하지 않습니다. 반응형 크기 변화는 media query로만 처리합니다.
- letter spacing은 `0`을 기본으로 유지합니다.
- KPI 숫자는 굵게 표시하되 검정색으로 유지합니다.

## 반응형
- 데스크톱: topbar 2열, KPI 4열, chart grid 2열을 기본으로 합니다.
- 태블릿 이하: topbar와 주요 콘텐츠는 1열로 전환합니다.
- 모바일: KPI, drivers, evidence는 1열로 전환하고, 탭은 가로 스크롤을 허용합니다.
- 모든 viewport에서 가로 overflow가 없어야 합니다.
- 버튼/탭 텍스트는 줄바꿈 또는 가로 스크롤로 처리하고, UI 요소끼리 겹치면 안 됩니다.

## Evidence 규칙
- Evidence 탭은 선택 사항이 아닙니다.
- `04_metrics.json`의 KPI 이름, 계산식, 값, 상태를 표시합니다.
- `05_analysis.py` 재현 가능 여부를 표시합니다.
- `05_analysis.ipynb` 노트북 생성 여부와 분석가용 해석 흐름을 표시합니다.
- `08_validation_report.md`가 있으면 수치 일관성, 재현성, 해석 리스크를 표시합니다.
- `08_validation_report.md`가 아직 없으면 stage 7에서 검증 예정임을 표시합니다.
- 결측, 중복, 표본 제한, 인과 해석 제한은 숨기지 않습니다.

## 금지
- KPI 수치에 색상 적용
- `border-left` 등 한쪽 변만 있는 border
- 외부 chart/font CDN 의존성
- 기본 이모지 사용
- 이유 없는 파이 차트 / 3D 차트
- 한 탭에 차트 8개 이상
- 분석에서 나오지 않은 지표 임의 추가
- Evidence 없이 숫자만 보여주는 화면
- 화면 전체를 검은색, 보라색, 베이지색 계열 하나로 몰아가는 단색 테마
