---
name: ai-analyst-pipeline
description: Run-scoped AI data analysis pipeline for Codex. Use when the user asks to analyze CSV/Excel/JSON/TSV/PDF data, create analyst-ready EDA/KPI/reproducible Python/notebook/dashboard/report outputs, handle multiple data files, or manage ai-analyst-pipeline runs and outputs.
---

# ai-analyst-pipeline

Run a 7-stage, analyst-ready data analysis pipeline and keep every execution under a durable run folder.

## Required Runtime Flow

1. Resolve the plugin root as the folder containing `.codex-plugin/plugin.json`.
2. Create a run with `python3 scripts/ai_pipeline.py create-run --path <source-file>`.
3. Record these values from the command output:
   - `run_id`
   - `run_dir`
   - `output_dir`
   - `source_files[].path`
4. Execute the stages in order. Do not parallelize dependent stages.
5. Before each stage, check whether all expected outputs for that stage already exist in the current run. If they exist, mark that stage cached and skip it.
6. After each stage, verify every expected output file exists before starting the next stage.
7. Use `python3 scripts/ai_pipeline.py write-progress --status running --current-step <N>` while a stage is active, and mark failed/complete explicitly.
8. At the end, run `python3 scripts/ai_pipeline.py validate-outputs`.

## Stages

| No | Stage | Reference prompt(s) | Output(s) |
|----|-------|---------------------|-----------|
| 1 | Data contract & profile | `references/agents/data-contract.md`, `references/agents/data-ingestion.md` | `00_data_contract.md`, `01_dataset_profile.md` |
| 2 | Analysis plan & EDA | `references/agents/analysis-plan.md`, `references/agents/eda.md` | `02_analysis_plan.md`, `02_eda_report.md` |
| 3 | Problem definition | `references/agents/problem.md` | `03_problem_definition.md` |
| 4 | KPI summary & metrics JSON | `references/agents/metrics.md` | `04_kpi_summary.md`, `04_metrics.json` |
| 5 | Deep analysis & reproducible notebook | `references/agents/analysis.md`, `references/agents/reproducible-analysis.md` | `05_analysis.py`, `05_analysis.ipynb`, `05_analysis_report.md` |
| 6 | HTML dashboard | `references/agents/dashboard.md` | `06_dashboard.html` |
| 7 | Executive & validation reports | `references/agents/report.md`, `references/agents/validation.md` | `07_executive_report.md`, `08_validation_report.md` |

## Helper CLI

Run from the plugin root, or use an absolute path to `scripts/ai_pipeline.py`.

```bash
python3 scripts/ai_pipeline.py create-run --path /path/to/data.csv
python3 scripts/ai_pipeline.py status
python3 scripts/ai_pipeline.py workflow-status
python3 scripts/ai_pipeline.py list-inputs
python3 scripts/ai_pipeline.py list-outputs
python3 scripts/ai_pipeline.py read-output --name 07_executive_report.md
python3 scripts/ai_pipeline.py reset-run
python3 scripts/ai_pipeline.py validate-outputs
python3 scripts/ai_pipeline.py template-path
```

Set `AI_PIPELINE_RUNTIME_ROOT=/path/to/data-ai-pipeline` only when the user wants a non-default workspace.
The default workspace is `~/Documents/data-ai-pipeline`.

## Quality Rules

- Use only source-file evidence. Do not invent metrics.
- Write generated reports and visible dashboard text in Korean by default unless the user explicitly asks for another language. Preserve source column names, file names, formulas, code identifiers, and proper nouns when accuracy requires it.
- For multiple files, create `00_data_contract.md` first and decide whether to use one file, concatenate, join, analyze separately, or hold the relationship as uncertain. Never force a join without grain/key evidence.
- Define KPI names, formulas, units, and comparison baselines before deep analysis.
- Store machine-readable core metrics in valid JSON at `04_metrics.json`; do not wrap JSON in Markdown fences.
- Write `05_analysis.py` so core report/dashboard numbers are reproducible from the original source paths, and write `05_analysis.ipynb` as the analyst-facing notebook with Korean markdown interpretation and executable code cells.
- End with `08_validation_report.md` covering missing outputs, numeric consistency, reproducibility, dashboard quality, and interpretation risks.
- Do not mix absolute, relative, and cumulative values without labels.
- Warn when sample size is small or data quality limits confidence.
- Build dashboard output from `assets/templates/dashboard-sample.html` using the `Overview`, `Drivers`, `Scenario`, `Evidence` tab contract. Keep `Scenario` when the data supports what-if analysis, model threshold comparison, top-N/capacity tradeoffs, or segment/rule comparison such as target size versus observed event rate. Do not present rule scenarios as causal effect forecasts unless intervention outcome data exists.
- Keep dashboard charts question-driven and SVG/Canvas-only. Do not use CDN chart libraries or external fonts.
- Keep KPI numbers black; use color only for status labels or visual marks.
- Keep `Evidence` visible with metric definitions, `05_analysis.py` and `05_analysis.ipynb` reproducibility status, validation-pending/validation summary, and data-quality limits.

## Completion Standard

Final output must include:

- Run ID
- Source file path(s)
- Output directory
- The expected artifact paths, with cached markers where applicable
- Validation result from `validate-outputs`
- Any failed, skipped, or unverified stages
