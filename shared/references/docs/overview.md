# ai-pipeline-kit

데이터 파일 경로 하나 이상으로 7단계 AI 분석 파이프라인을 순차 실행하고, 재현 가능한 분석 코드, Jupyter Notebook, 대시보드, 임원 보고서, 검증 리포트까지 생성하는 툴킷.

CSV · Excel · JSON · TSV · PDF 등 형식 무관 — 데이터 파일 경로만 주면 됩니다.

자세한 사용법은 [usage.md](./usage.md) 참고.

## 역할

이 키트는 7개 단계의 전문 AI 에이전트를 순서대로 지휘하는 **데이터 분석 오케스트레이터**입니다.

핵심 목표:
- 여러 파일의 grain, 키, 결합 가능성을 먼저 계약으로 정의
- 데이터 구조와 품질을 진단
- 분석 계획과 성공 기준을 사전에 명시
- 문제 정의 → KPI 설계 → 심층 분석 → 대시보드 → 임원 보고서 순서로 진행
- 핵심 KPI를 `04_metrics.json`으로 저장하고 `05_analysis.py`와 `05_analysis.ipynb`로 재현 가능하게 유지
- 최종 `08_validation_report.md`에서 수치 일관성과 해석 리스크를 검증
- 실행 1회마다 run 폴더를 만들어 산출물과 진행 상태를 보존
- 원본 데이터는 복사하지 않고 직접 경로를 `run.json`에 기록
- 근거 없는 수치 생성 없이 입력 데이터 기반으로 분석

## 스킬 목록

| 스킬 | 역할 |
|------|------|
| `run-pipeline` | 7단계 분석 파이프라인 순차 실행 (run 단위 산출물 관리) |
| `dashboard-design` | AI Pipeline 전용 대시보드 디자인 시스템 |
| `visualize` | 인사이트 → 질문 중심 HTML 대시보드 제작 |

## 파이프라인 구조

```text
원본 데이터 파일 경로
  → 새 run 생성: /Users/eunsu/Documents/data-ai-pipeline/runs/<run_id>/
  → @data-contract   (파일 관계 + grain + 조인/결합 전략)
  → @data-ingestion  (데이터 구조 파악 + 품질 진단)
  → @analysis-plan   (분석 질문 + 방법론 + 성공 기준)
  → @eda             (탐색적 데이터 분석)
  → @problem         (핵심 문제 정의)
  → @metrics         (KPI 설계 + metrics.json)
  → @analysis        (심층 분석 + 재현 Python + Jupyter Notebook)
  → @dashboard       (HTML 대시보드 생성)
  → @report          (임원용 보고서 + 최종 검증)
```

| 단계 | 에이전트 | 산출물 |
|------|---------|--------|
| 1 | `@data-contract`, `@data-ingestion` | `00_data_contract.md`, `01_dataset_profile.md` |
| 2 | `@analysis-plan`, `@eda` | `02_analysis_plan.md`, `02_eda_report.md` |
| 3 | `@problem` | `runs/<run_id>/outputs/03_problem_definition.md` |
| 4 | `@metrics` | `04_kpi_summary.md`, `04_metrics.json` |
| 5 | `@analysis`, `@reproducible-analysis` | `05_analysis.py`, `05_analysis.ipynb`, `05_analysis_report.md` |
| 6 | `@dashboard` | `runs/<run_id>/outputs/06_dashboard.html` |
| 7 | `@report`, `@validation` | `07_executive_report.md`, `08_validation_report.md` |

## 설치 및 사용 방법

### 파일 경로 직접 입력

AI 에이전트 채팅창에 파일 경로와 함께 입력:

```text
파이프라인 실행해줘 /Users/eunsu/Desktop/sales.csv
```

Codex helper 기준으로는 `python3 scripts/ai_pipeline.py create-run --path <파일경로>`로 run을 만들고, 이후 모든 산출물을 해당 run의 `outputs/`에 저장합니다.

## 런타임 데이터 구조

```text
/Users/eunsu/Documents/data-ai-pipeline/
  .latest_run_id
  runs/
    <run_id>/
      run.json
      progress.json
      outputs/
        00_data_contract.md
        01_dataset_profile.md
        02_analysis_plan.md
        02_eda_report.md
        03_problem_definition.md
        04_kpi_summary.md
        04_metrics.json
        05_analysis.py
        05_analysis.ipynb
        05_analysis_report.md
        06_dashboard.html
        07_executive_report.md
        08_validation_report.md
```

`run.json`에는 원본 파일 경로와 파일 metadata가 저장됩니다. 원본 데이터 파일은 별도 input 폴더로 복사하지 않습니다.

## 산출물

결과물은 최신 run 기준 `/Users/eunsu/Documents/data-ai-pipeline/runs/<run_id>/outputs/` 에 생성됩니다.

| 파일 | 설명 |
|------|------|
| `00_data_contract.md` | 원본 파일 인벤토리, grain, 다중 파일 결합/분리 전략 |
| `01_dataset_profile.md` | 데이터 구조 + 품질 진단 |
| `02_analysis_plan.md` | 분석 질문, 방법론, 성공 기준, 검증 계획 |
| `02_eda_report.md` | 탐색적 분석 결과 |
| `03_problem_definition.md` | 핵심 문제 정의 |
| `04_kpi_summary.md` | KPI 설계 및 계산 기준 |
| `04_metrics.json` | 보고서/대시보드와 맞출 기계 판독용 KPI 값 |
| `05_analysis.py` | 핵심 수치를 재계산하는 재현 Python 스크립트 |
| `05_analysis.ipynb` | 분석가가 열어볼 수 있는 Jupyter Notebook |
| `05_analysis_report.md` | 심층 분석 보고서 |
| `06_dashboard.html` | 인터랙티브 HTML 대시보드 |
| `07_executive_report.md` | 임원용 요약 보고서 |
| `08_validation_report.md` | 수치 일관성, 재현성, 해석 리스크 검증 |

개별 단계만 재실행: `"3단계부터 다시 해줘"` 또는 `"@eda 만 다시 실행해줘"`
전체 재실행: `"처음부터 다시 실행해줘"` — 새 run 생성

## 실행 규칙

- **단계 간 병렬 실행 금지** — 반드시 순서대로 실행
- 이전 단계 산출물 파일이 현재 run의 `outputs/`에 존재해야 다음 단계 시작
- 체크포인트 캐싱 — 현재 run에서 이미 완료된 단계는 자동 스킵 (`cached` 표시)
- 단계 실패 시 해당 단계에서 즉시 중단 후 사용자에게 보고
- 전체 완료 후 결과물 경로 목록 출력
- 사용자가 요청했거나 현재 작업 맥락상 명확할 때만 전체 성공 및 산출물 검증 완료 후 결과 폴더를 로컬 앱으로 열기
- 모든 산출물은 기본 한글로 작성 — 단, 원본 컬럼명·파일명·계산식·코드 식별자는 정확성을 위해 유지
- 도메인 독립적 — 커머스 전용 가정을 타 도메인에 강제하지 않음
- 근거 없는 수치 생성 금지

## 분석 품질 원칙

모든 에이전트에 공통 적용됩니다.

- **KPI 정의가 먼저** — 이름, 계산 기준, 단위를 확정한 뒤 분석
- **다중 파일은 계약 먼저** — grain과 키가 확인되기 전에는 자동 조인하지 않음
- **지표는 JSON으로도 저장** — `04_metrics.json`이 보고서와 대시보드 수치의 기준
- **재현 가능한 분석** — 핵심 수치는 `05_analysis.py`로 다시 계산 가능하고 `05_analysis.ipynb`에서 분석 흐름을 확인할 수 있어야 함
- **절대값 / 상대값 / 누적값 혼용 금지**
- **차트는 질문에 답한다** — 예쁨보다 명확함 우선
- **카드 제목은 결론형 또는 질문형** — `매출 현황`이 아니라 `왜 마진이 낮은가?`
- **임원용 요약과 실무자용 상세는 분리**
- **표본이 작으면 반드시 경고**
- **산출물은 기본 한글 작성** — 사용자가 다른 언어를 요청하지 않는 한 보고서와 대시보드 문구는 한글로 작성
- **도메인 독립성** — 커머스 전용 가정을 타 도메인에 강제하지 않음

상세 규칙 파일:
- `references/rules/analysis-principles.md`
- `references/rules/design-system.md`

## 대시보드 템플릿 규칙

`@dashboard`는 반드시 `dashboard-sample.html`을 베이스 템플릿으로 사용합니다.

- 새 HTML 구조를 처음부터 작성하지 않음
- 템플릿의 `—` 플레이스홀더와 SVG 수치만 실제 분석 결과로 교체
- 순수 SVG/Canvas만 사용 — Chart.js, D3 등 CDN 라이브러리 금지
- KPI 수치에는 색상 적용 금지
- 기본 이모지 사용 금지 — 아이콘이 필요하면 인라인 SVG 사용
- 대시보드 디자인 상세는 `dashboard-design` 스킬과 `skills/dashboard-design/references/design-tokens.md` 참고

## Codex 통합 기준

Codex에서는 이 프로젝트를 **로컬 플러그인 + 번들 스킬 + helper CLI** 형태로 사용합니다.

설치 위치:

```bash
<marketplace-root>/plugins/ai-pipeline-kit/
```

런타임 데이터 위치:

```bash
/Users/eunsu/Documents/data-ai-pipeline/
```

현재 스킬 기준 구조:

```text
skills/
  run-pipeline/SKILL.md
  dashboard-design/SKILL.md
  visualize/SKILL.md
```

Codex에서 사용할 때는 plugin skill을 직접 읽어 실행할 수 있습니다.

```text
ai-pipeline-kit로 /Users/eunsu/Desktop/sales.csv 분석해줘
run-pipeline로 latest run 이어서 진행해줘
visualize로 분석 결과를 대시보드로 만들어줘
```

프로젝트 설명과 운영 규칙은 이 README와 각 스킬 파일을 기준으로 관리합니다.
