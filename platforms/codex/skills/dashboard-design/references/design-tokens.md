# Design Tokens & Component Spec

## 색상 팔레트

### CSS 변수 (`:root`)
```css
--bd:  rgba(110,93,80,0.16)
--bds: rgba(96,79,67,0.24)
--offwhite: rgba(247,244,239,0.97)
--lavender: rgba(237,231,245,0.96)
--mint:     rgba(225,241,236,0.96)
--rose:     rgba(247,229,235,0.96)
--cream:    rgba(247,241,226,0.96)
--beige:    rgba(239,232,223,0.97)
--acc: #4fb799
--dk:  #2f2b27
--mu:  #766c63
--so:  #9a9086
```

### 상태 색상
| 상태 | 컬러 |
|------|------|
| 좋음/성공 | `#35c995` / `#218d72` |
| 나쁨/위험 | `#ef7d86` / `#9b2d38` |
| 경고/보통 | `#efb05d` / `#a0620a` |
| 정보/중립 | `#5b8ef0` / `#3b5bbf` |

## 타이포그래피
```html
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```
| 용도 | 폰트 | 사이즈 |
|------|------|--------|
| 본문, 레이블 | Inter | 11–13px |
| KPI 수치 | Barlow 600 | 16–26px |
| 대시보드 제목 | Barlow | 24px |
| 이탤릭 서브타이틀 | Instrument Serif italic | 동일 |
| 코드형 레이블 | JetBrains Mono | 9–11px |

## 레이아웃 구조
```
body (background: #000, padding: 32px 40px 80px)
└─ .tab-bar
└─ .dash-panel(.active)
   └─ .dash (offwhite, border-radius: 20px)
      ├─ .dash-topbar (검정 헤더)
      └─ .dash-body (padding: 22px)
         ├─ .story-block (4칸 내러티브)
         ├─ .dash-step-hdr (STEP N)
         ├─ .dash-kpi-row (KPI 4열)
         ├─ .dash-charts (차트 그리드)
         ├─ .sim-widget (시뮬레이터)
         └─ .dash-actions (액션 3열)
```

## 컴포넌트 HTML 패턴

### Tab Bar
```html
<div class="tab-bar">
  <div class="tab-btn active" onclick="switchTab(0)">탭명</div>
</div>
```

### KPI Row
```html
<div class="dash-kpi-row">
  <div class="dk-box">
    <div class="dk-lbl">레이블</div>
    <div class="dk-val">$396K</div>
    <div class="dk-delta up">↑ 설명</div>
  </div>
</div>
```

### Story Flow (4칸)
```html
<div class="story-block"><div class="story-flow">
  <div class="sf-cell">
    <div class="sf-label lbl-now">현황</div>
    <div class="sf-val">핵심 수치</div>
    <div class="sf-desc">설명</div>
  </div>
  <!-- lbl-why / lbl-so / lbl-act -->
</div></div>
```

### Chart Card
```html
<div class="dash-charts">  <!-- three-eq / full -->
  <div class="chart-card">
    <div class="cc-title">결론형 제목</div>
    <div class="cc-desc">해석 1~2줄</div>
    <svg viewBox="0 0 320 190" width="100%" height="auto">...</svg>
  </div>
</div>
```

### Simulation Widget
```html
<div class="sim-widget">
  <div class="sim-title">제목 <span class="sim-badge">SIMULATION</span></div>
  <div class="sim-slider-row">
    <input type="range" class="sim-range" min="0" max="100" value="50" oninput="updateSim(this)">
  </div>
</div>
```

### Action Items
```html
<div class="dash-actions">
  <div class="da-item">
    <div class="da-p">P1 — 즉시</div>
    <div class="da-title">액션</div>
    <div class="da-why">근거</div>
  </div>
</div>
```

## SVG 차트 규칙
- 축선: `stroke="rgba(96,79,67,.15)"` / 그리드: `stroke-dasharray="4,3"`
- 바 색: 좋음 `#35c995` / 나쁨 `#ef7d86` / 정보 `#5b8ef0` / 경고 `#efb05d`
- 값 레이블: `font-size="11"` + `text-anchor="middle"` + `font-weight="700"`
- 축 레이블: `font-size="10"` + `fill="var(--mu)"`
- `svg text { font-family: 'Inter', sans-serif; font-style: normal; }` 전역 적용

## JS 탭 전환
```js
function switchTab(i) {
  document.querySelectorAll('.tab-btn').forEach((b,j) => b.classList.toggle('active', i===j));
  document.querySelectorAll('.dash-panel').forEach((p,j) => p.classList.toggle('active', i===j));
}
```

## 반응형
```css
@media (max-width: 1100px) { .dash-charts, .dash-charts.three-eq { grid-template-columns: 1fr; } }
@media (max-width: 700px) { .dash-kpi-row { grid-template-columns: 1fr 1fr; } .dash-actions { grid-template-columns: 1fr; } }
```
