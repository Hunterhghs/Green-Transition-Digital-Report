# Green Transition Digital Report

A professional-grade digital report on the global green transition, built as a single-page consulting document.

**Central claim:** the green transition has cleared the technology hurdle and now faces a capital-allocation problem — where money, grid capacity, and mineral processing can be built, not what technology exists.

## Structure

- Executive summary
- Clean energy investment ($2T in 2025, IEA)
- Cost deflation and clean-technology manufacturing
- Power systems and the grid bottleneck
- Policy architecture (IRA, CBAM, industrial policy)
- Critical minerals and supply-chain geopolitics
- Counter-case: affordability and fragmentation
- Regional scoreboard (China, EU, US, India, Global South)
- 2030 outlook with emissions trajectories
- Sources and methodology

## Technical notes

- Self-contained `index.html`; the only external dependency is Chart.js via CDN for the five interactive figures.
- Verified with the Veles Phase-4 gate: HTML parse, anchor integrity, chart-canvas wiring, external link hygiene, CJK-leak scan, content density, binding-term presence, and the english-report-writing `prose_lint.py` (0 errors, 0 warnings).
- Consulting aesthetic: editorial serif typography, hairline rules, KPI band, takeaway boxes, footnote-style sourcing.

## Deploy

Push to `main`; GitHub Pages serves the repository root.
