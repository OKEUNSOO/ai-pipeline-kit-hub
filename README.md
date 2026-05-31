# ai-pipeline-kit-hub

CSV·Excel·JSON·TSV·PDF 파일을 7단계 AI 분석 파이프라인으로 처리하는 스킬 허브.  
Claude Code, Codex, Hermes, OpenClaw, Gemini CLI 모두 지원합니다.

## 설치

```bash
git clone https://github.com/OKEUNSOO/ai-pipeline-kit-hub
cd ai-pipeline-kit-hub
chmod +x install.sh
./install.sh
```

설치된 플랫폼을 자동 감지하여 각 경로에 스킬을 설치합니다.

## 수동 설치

| 플랫폼 | 스킬 파일 위치 | 공유 리소스 |
|--------|--------------|------------|
| Claude Code | `~/.claude/plugins/ai-pipeline-kit/skills/` | `shared/` 링크 |
| Codex | `~/.codex/plugins/ai-pipeline-kit/` | `shared/` 링크 |
| Hermes | `~/.hermes/skills/ai-pipeline-kit/` | `shared/` 링크 |
| OpenClaw | `~/.openclaw/skills/ai-pipeline-kit/` | `shared/` 링크 |
| Gemini CLI | `~/.gemini/skills/ai-pipeline-kit/` | `shared/` 링크 |

## 사용법

```text
ai-pipeline-kit으로 /path/to/data.csv 분석해줘
```

## 파이프라인 단계

| 단계 | 산출물 |
|------|--------|
| 1 | 데이터 계약 + 데이터셋 프로파일 |
| 2 | 분석 계획 + EDA |
| 3 | 문제 정의 |
| 4 | KPI 요약 + metrics.json |
| 5 | 재현 Python + Jupyter Notebook + 분석 보고서 |
| 6 | HTML 대시보드 |
| 7 | 임원 보고서 + 검증 리포트 |

산출물은 `~/Documents/data-ai-pipeline/runs/<run_id>/outputs/`에 저장됩니다.

## 구조

```
ai-pipeline-kit-hub/
├── shared/             # 공통 리소스 (scripts, references, assets)
├── platforms/
│   ├── claude/         # Claude Code 스킬 (4개)
│   ├── codex/          # Codex 플러그인 (4개 스킬 + plugin.json)
│   ├── hermes/         # Hermes 스킬
│   ├── openclaw/       # OpenClaw 스킬
│   └── gemini/         # Gemini CLI 스킬
├── install.sh
└── README.md
```
