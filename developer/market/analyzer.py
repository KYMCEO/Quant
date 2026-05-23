#!/usr/bin/env python3
"""
AI Stock Factory — 시황 자동 분석기
수집된 데이터 → 핵심 인사이트 텍스트 생성
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR   = Path(__file__).parent.parent.parent / "data" / "market"
REPORT_DIR = Path(__file__).parent.parent.parent / "data" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_latest():
    latest = DATA_DIR / "latest.json"
    if not latest.exists():
        raise FileNotFoundError("latest.json 없음 — collector.py 먼저 실행하세요")
    with open(latest, encoding="utf-8") as f:
        return json.load(f)


def _signal(pct):
    if pct >= 2:    return "🟢 강세"
    if pct >= 0.5:  return "🔼 상승"
    if pct >= -0.5: return "➡️  보합"
    if pct >= -2:   return "🔽 하락"
    return "🔴 급락"


def analyze(data):
    lines = []
    date = data["collected_at"][:10]
    lines.append(f"# 📊 AI Stock Factory 시황 브리핑 — {date}\n")

    # 나스닥 섹션
    lines.append("## 🇺🇸 미국 시장\n")
    for name, v in data.get("nasdaq", {}).items():
        if "error" in v:
            continue
        sig = _signal(v["change_pct"])
        lines.append(f"- **{name}** ({v['ticker']}) {v['close']:,}  {sig} ({v['change_pct']:+.2f}%)")

    # 코스피 섹션
    lines.append("\n## 🇰🇷 한국 시장\n")
    for name, v in data.get("kospi_index", {}).items():
        if "error" in v:
            continue
        sig = _signal(v["change_pct"])
        lines.append(f"- **{name}** {v['close']:,}  {sig} ({v['change_pct']:+.2f}%)")
    for name, v in data.get("kospi", {}).items():
        if "error" in v:
            continue
        sig = _signal(v["change_pct"])
        lines.append(f"- **{name}** ({v['code']}) {v['close']:,}원  {sig} ({v['change_pct']:+.2f}%)")

    # 핵심 인사이트 자동 생성
    lines.append("\n## 🔍 핵심 인사이트\n")

    nasdaq_data = {k: v for k, v in data.get("nasdaq", {}).items() if "error" not in v}
    movers_up   = sorted(nasdaq_data.items(), key=lambda x: x[1]["change_pct"], reverse=True)[:2]
    movers_down = sorted(nasdaq_data.items(), key=lambda x: x[1]["change_pct"])[:2]

    if movers_up:
        top = movers_up[0]
        lines.append(f"- 오늘 가장 강한 종목: **{top[0]}** ({top[1]['change_pct']:+.2f}%)")
    if movers_down:
        bot = movers_down[0]
        lines.append(f"- 오늘 가장 약한 종목: **{bot[0]}** ({bot[1]['change_pct']:+.2f}%)")

    # 규제 격차 테마 연결
    lines.append("\n## 🎯 AI Stock Factory 테마 연결\n")
    theme_names = ["AI인프라(GRID)", "클린에너지(ICLN)", "배터리ESS(LIT)"]
    for name in theme_names:
        v = nasdaq_data.get(name)
        if v:
            sig = _signal(v["change_pct"])
            lines.append(f"- **{name}** {v['change_pct']:+.2f}%  {sig}")

    lines.append(f"\n---\n_수집: {data['collected_at']} | AI Stock Factory 자동 분석_")

    return "\n".join(lines)


def run():
    data   = load_latest()
    report = analyze(data)

    date_str  = datetime.now().strftime("%Y-%m-%d")
    out_file  = REPORT_DIR / f"{date_str}_briefing.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(report)

    # 최신 리포트도 덮어쓰기
    latest_report = REPORT_DIR / "latest_briefing.md"
    with open(latest_report, "w", encoding="utf-8") as f:
        f.write(report)

    import sys
    print(f"report saved: {out_file}")
    sys.stdout.buffer.write(report.encode("utf-8", errors="replace"))
    sys.stdout.buffer.write(b"\n")
    return report


if __name__ == "__main__":
    run()
