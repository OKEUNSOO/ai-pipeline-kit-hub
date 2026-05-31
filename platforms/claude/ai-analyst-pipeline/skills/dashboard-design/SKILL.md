---
name: dashboard-design
description: AI Pipeline Dashboard design system. Color tokens, typography, layout patterns, and component specs for consistent dashboard output.
---

# Dashboard Design Skill

`assets/templates/dashboard-sample.html` 기준 디자인 시스템.
HTML 컴포넌트·CSS 변수·JS 코드·SVG 패턴이 필요할 때는 `references/design-tokens.md`를 Read 도구로 읽어서 사용한다.

---

## 핵심 원칙

- **배경**: 외부 `#000`, 내부 카드 `rgba(250,246,240,.97)`
- **KPI 수치**: 반드시 `#0a0a0a` 검정 — 색상 절대 금지
- **상태**: 좋음 `#35c995` / 나쁨 `#ef7d86` / 경고 `#efb05d`
- **차트**: 순수 SVG만 — CDN 라이브러리 금지
- **이모지**: 완전 금지 — SVG 아이콘으로만 대체

## 차트 카드 규칙

```css
.chart-card { max-height: 380px; display: flex; flex-direction: column; padding: 20px; }
.chart-card.primary { max-height: 440px; }
.dash-charts.full .chart-card { max-height: none; }
.chart-card svg { width: 100%; height: auto; max-height: none; margin-top: 8px; }
.dash-charts { align-items: stretch; }
```

- SVG viewBox 내부 플롯 영역은 viewBox 면적의 **80% 이상** 차지
- 여백: 상하 10px, 좌우 축 레이블 있으면 40~70px
- 바 차트 `rect`: `y = (1 - v/max) * h`, `height = (v/max) * h`

## 레이아웃

- `.dash-charts` → 2열 / `.three-eq` → 3열 / `.full` → 1열
- 메인 차트 행은 `1.5fr 1fr` 비율 권장 (동등 분할 지양)
- `.full` 은 탭당 1개만
- 카드 계층: `.primary` (메인) / 일반 / `.muted` (보조)

## 타이포

- 차트 제목 `.cc-title`: Inter 700 — **한글 포함 시 serif 금지**
- KPI 수치: Barlow 600
- 차트 레이블·수치: JetBrains Mono
- Instrument Serif italic: **영문 전용** (헤더 서브타이틀만)

## 금지

- KPI 수치에 색상 / 한쪽 변만 있는 border / 기본 이모지
- CDN 차트 라이브러리 / 파이·3D 차트 / 탭당 차트 8개 이상

## 출력

완성 파일: `<AI_PIPELINE_OUTPUT_DIR>/06_dashboard.html`

> 상세 HTML 패턴, CSS 변수, JS 코드가 필요하면 `references/design-tokens.md`를 Read 도구로 읽어서 사용한다.
