---
name: run-pipeline
description: 원본 데이터 파일 경로를 받아 run 단위 7단계 AI 분석 파이프라인을 순서대로 실행하고 재현 코드, Jupyter Notebook, 대시보드, 보고서, 검증 리포트를 생성합니다. CSV·Excel·JSON·TSV·PDF 등 형식 무관.
---

# /run-pipeline

입력: `$ARGUMENTS`

CSV, Excel, JSON, TSV, PDF 등 형식 무관 — 1단계 Data Contract/Profile에서 자동 감지합니다.

## 핵심 런타임 구조

ai-analyst-pipeline은 input 폴더로 파일을 복사하지 않는다.
원본 파일은 사용자가 준 직접 경로를 그대로 읽고, 실행 1회마다 run 폴더를 만든다.
모든 산출물은 기본 한글로 작성한다. 단, 원본 컬럼명·파일명·계산식·코드 식별자는 정확성을 위해 그대로 유지한다.

```text
/Users/eunsu/Documents/data-ai-pipeline/
  .latest_run_id
  runs/
    <run_id>/
      run.json          # 원본 source file 경로/크기/mtime metadata
      progress.json     # workflow 진행 상태
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

## 실행 전 체크

Codex에서는 plugin root(`.codex-plugin/plugin.json`이 있는 폴더)의 `scripts/ai_pipeline.py` helper CLI를 우선 사용한다.

1. `$ARGUMENTS` 에 분석할 원본 파일 경로가 있는지 확인한다.
2. 파일 경로가 있으면 `python3 scripts/ai_pipeline.py create-run --path <파일경로>`로 새 run을 만든다.
3. 파일 경로가 없으면 사용자에게 안내하고 **즉시 중단**한다:
   > "분석할 파일 경로를 입력해주세요. 예: 파이프라인 실행해줘 /Users/eunsu/Desktop/sales.csv"
4. `create-run` 결과에서 아래 값을 기억한다:
   - `run_id`
   - `run_dir`
   - `output_dir`
   - `source_files[].path`
5. 이후 모든 단계 작업에서 다음 값을 기준으로 사용한다:
   - `AI_PIPELINE_RUN_ID=<run_id>`
   - `AI_PIPELINE_RUN_DIR=<run_dir>`
   - `AI_PIPELINE_OUTPUT_DIR=<output_dir>`
   - `AI_PIPELINE_SOURCE_FILES=<source_files[].path 목록>`

## 체크포인트 규칙

각 단계 실행 **전** 아래 조건을 확인한다.

- 해당 단계의 산출물 파일이 모두 현재 run의 `outputs/` 아래에 존재하면 → `✅ STEP N — 완료 (skip)` 출력 후 건너뜀
- 하나라도 없으면 → 해당 단계 실행

**확인 방법 (bash):**
```bash
OUTPUT_A="$AI_PIPELINE_OUTPUT_DIR/00_data_contract.md"
OUTPUT_B="$AI_PIPELINE_OUTPUT_DIR/01_dataset_profile.md"

if [ -f "$OUTPUT_A" ] && [ -f "$OUTPUT_B" ]; then
  echo "✅ STEP 1 — 완료 (skip)"
else
  # 에이전트 실행
fi
```

> **강제 재실행:** 사용자가 "처음부터 다시"라고 하면 새 run을 만든다. 같은 run에서 다시 쓰고 싶으면 `python3 scripts/ai_pipeline.py reset-run`으로 현재 run의 outputs만 비운다.

## 단계별 실행 순서

각 단계는 체크포인트 확인 후, 실행이 필요한 경우에만 해당 reference prompt를 읽고 수행한다.

```text
STEP 1 → references/agents/data-contract.md + data-ingestion.md  출력: 00_data_contract.md, 01_dataset_profile.md
STEP 2 → references/agents/analysis-plan.md + eda.md             출력: 02_analysis_plan.md, 02_eda_report.md
STEP 3 → references/agents/problem.md         출력: 03_problem_definition.md
STEP 4 → references/agents/metrics.md         출력: 04_kpi_summary.md, 04_metrics.json
STEP 5 → references/agents/analysis.md + reproducible-analysis.md 출력: 05_analysis_report.md, 05_analysis.py, 05_analysis.ipynb
STEP 6 → references/agents/dashboard.md       출력: 06_dashboard.html
STEP 7 → references/agents/report.md + validation.md             출력: 07_executive_report.md, 08_validation_report.md
```

## 단계 완료 확인

각 단계 실행 후 현재 run의 `outputs/` 아래 산출물 파일 존재를 확인한다.
파일이 없으면 해당 단계 실패로 간주하고 사용자에게 보고 후 중단한다.

실행 중에는 `python3 scripts/ai_pipeline.py workflow-status` 또는 `python3 scripts/ai_pipeline.py status`로 상태를 확인한다.
상태 파일은 현재 run의 `progress.json`에 저장된다.

## Workflow 진행상황 표시

상태표 예시:

```text
AI Pipeline Workflow Status

Run ID: 20260513_163714_5268edc2
Output: /Users/eunsu/Documents/data-ai-pipeline/runs/20260513_163714_5268edc2/outputs
Status: running (2/7)

┌────┬──────────────────────┬────────────────────────────┬────────────┐
│ No │ Step                 │ Output                     │ Status     │
├────┼──────────────────────┼────────────────────────────┼────────────┤
│ 1  │ Data Contract/Profile │ 00_data_contract.md, 01_dataset_profile.md │ ✅ done    │
│ 2  │ Analysis Plan/EDA     │ 02_analysis_plan.md, 02_eda_report.md      │ 🔄 running │
│ 3  │ Problem Definition   │ 03_problem_definition.md   │ ⏳ pending │
│ 4  │ KPI Summary/Metrics  │ 04_kpi_summary.md, 04_metrics.json │ ⏳ pending │
│ 5  │ Reproducible Notebook & Analysis │ 05_analysis.py, 05_analysis.ipynb, 05_analysis_report.md │ ⏳ pending │
│ 6  │ Dashboard HTML       │ 06_dashboard.html          │ ⏳ pending │
│ 7  │ Executive/Validation │ 07_executive_report.md, 08_validation_report.md │ ⏳ pending │
└────┴──────────────────────┴────────────────────────────┴────────────┘
```

## 완료 후 폴더 열기

전체 파이프라인이 성공적으로 끝나면 산출물 폴더 경로를 최종 안내에 포함한다. 사용자가 로컬 앱으로 열기를 요청했거나 기존 작업 맥락상 명확하면 현재 run의 산출물 폴더에서 Antigravity를 연다.

```bash
cd "$AI_PIPELINE_OUTPUT_DIR" && antigravity .
```

- 명령은 파이프라인 성공 및 산출물 검증이 끝난 뒤 필요할 때 1회만 실행한다.
- 실패/중단 상태에서는 실행하지 않는다.
- 실행했다면 사용자에게는 `Antigravity로 산출물 폴더를 열었습니다: <AI_PIPELINE_OUTPUT_DIR>` 문구를 포함해 알린다.

## 완료 메시지

전체 성공 시 아래 형식으로 출력한다. skip한 단계는 `(cached)` 표시:

```text
✅ 파이프라인 완료

Run ID: <run_id>
Output: <AI_PIPELINE_OUTPUT_DIR>

📄 <AI_PIPELINE_OUTPUT_DIR>/00_data_contract.md     (cached)
📄 <AI_PIPELINE_OUTPUT_DIR>/01_dataset_profile.md   (cached)
📄 <AI_PIPELINE_OUTPUT_DIR>/02_analysis_plan.md     (cached)
📄 <AI_PIPELINE_OUTPUT_DIR>/02_eda_report.md        (cached)
📄 <AI_PIPELINE_OUTPUT_DIR>/03_problem_definition.md
📄 <AI_PIPELINE_OUTPUT_DIR>/04_kpi_summary.md
📄 <AI_PIPELINE_OUTPUT_DIR>/04_metrics.json
🐍 <AI_PIPELINE_OUTPUT_DIR>/05_analysis.py
📓 <AI_PIPELINE_OUTPUT_DIR>/05_analysis.ipynb
📄 <AI_PIPELINE_OUTPUT_DIR>/05_analysis_report.md
🌐 <AI_PIPELINE_OUTPUT_DIR>/06_dashboard.html
📄 <AI_PIPELINE_OUTPUT_DIR>/07_executive_report.md
📄 <AI_PIPELINE_OUTPUT_DIR>/08_validation_report.md
```
