# AI Pipeline Kit 사용법

파일 경로 하나 이상이면 분석 보고서 + 재현 Python + Jupyter Notebook + 인터랙티브 대시보드가 run 단위로 생성됩니다.

---

## 방법 1 — 파일 경로 직접 입력 (권장)

1. AI 에이전트 채팅창에 파일 경로와 함께 입력:
   ```text
   파이프라인 실행해줘 /Users/eunsu/Desktop/sales.csv
   ```
2. 플러그인이 새 run을 만들고 원본 파일 경로를 `run.json`에 기록합니다.
3. 결과물은 해당 run의 `outputs/` 폴더에 생성됩니다.
4. 완료 후 에이전트가 run ID, 산출물 폴더, 검증 결과를 알려줍니다.

원본 데이터 파일은 `/input` 폴더로 복사하지 않습니다. 사용자가 준 직접 경로를 그대로 읽습니다.

---

## 방법 2 — 터미널 helper

Codex plugin root에서 실행:

```bash
python3 scripts/ai_pipeline.py create-run --path ~/Desktop/내데이터.csv
python3 scripts/ai_pipeline.py create-run --source-path ~/Desktop/orders.csv --source-path ~/Desktop/customers.csv
python3 scripts/ai_pipeline.py workflow-status
```

---

## 결과물 위치

```text
/Users/eunsu/Documents/data-ai-pipeline/
└── runs/
    └── <run_id>/
        ├── run.json
        ├── progress.json
        └── outputs/
            ├── 00_data_contract.md
            ├── 01_dataset_profile.md
            ├── 02_analysis_plan.md
            ├── 02_eda_report.md
            ├── 03_problem_definition.md
            ├── 04_kpi_summary.md
            ├── 04_metrics.json
            ├── 05_analysis.py
            ├── 05_analysis.ipynb
            ├── 05_analysis_report.md
            ├── 06_dashboard.html       ← 인터랙티브 대시보드
            ├── 07_executive_report.md
            └── 08_validation_report.md
```

최신 run ID는 아래 파일에 저장됩니다.

```text
/Users/eunsu/Documents/data-ai-pipeline/.latest_run_id
```

---

## 입력 파일 관리 방식

이전 방식:
- `<runtime>/input/` 에 파일 복사
- `<runtime>/output/` 에 결과 덮어쓰기

현재 방식:
- 원본 파일은 복사하지 않음
- `run.json`에 원본 경로, 파일명, 크기, 수정 시간을 기록
- 여러 파일이면 `00_data_contract.md`에서 단일 파일/세로 결합/조인/별도 분석 전략을 먼저 결정
- 산출물은 `runs/<run_id>/outputs/`에 저장
- 실행 기록이 run 단위로 남으므로 이전 결과와 비교 가능

---

## 참고

- CSV, Excel, JSON, TSV, PDF 모두 가능
- `"3단계부터 다시 해줘"` 처럼 특정 단계만 재실행 가능
- 전체 운영 기준은 `README.md`와 `skills/run-pipeline/SKILL.md` 참고
