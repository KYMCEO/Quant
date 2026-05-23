#!/usr/bin/env python3
"""
AI Stock Factory — 시황 데이터 수집기
무료 소스: yfinance(나스닥/S&P500) + pykrx(코스피/코스닥)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import yfinance as yf
from pykrx import stock as krx

OUTPUT_DIR = Path(__file__).parent.parent.parent / "data" / "market"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ── 수집 대상 ──────────────────────────────────────────────

NASDAQ_TICKERS = {
    "나스닥 지수":    "^IXIC",
    "S&P500":        "^GSPC",
    "반도체(SOX)":   "^SOX",
    "엔비디아":      "NVDA",
    "AMD":           "AMD",
    "마이크로소프트": "MSFT",
    "넥스트에라에너지": "NEE",
    "버티브":        "VRT",
    "퀀타서비스":    "PWR",
}

KOSPI_TICKERS = {
    "삼성전자":  "005930",
    "SK하이닉스": "000660",
    "한국전력":  "015760",
    "LS일렉트릭": "010120",
    "HD현대일렉트릭": "267260",
}

THEME_ETFS = {
    "AI인프라(GRID)":    "GRID",
    "클린에너지(ICLN)":  "ICLN",
    "데이터센터(DTCR)":  "DTCR",
    "배터리ESS(LIT)":    "LIT",
}


# ── 수집 함수 ──────────────────────────────────────────────

def _pct(current, prev):
    if prev and prev != 0:
        return round((current - prev) / prev * 100, 2)
    return 0.0


def collect_nasdaq():
    results = {}
    for name, ticker in {**NASDAQ_TICKERS, **THEME_ETFS}.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            if len(hist) < 1:
                continue
            close = round(float(hist["Close"].iloc[-1]), 2)
            prev  = round(float(hist["Close"].iloc[-2]), 2) if len(hist) >= 2 else close
            results[name] = {
                "ticker":  ticker,
                "close":   close,
                "change_pct": _pct(close, prev),
            }
        except Exception as e:
            results[name] = {"ticker": ticker, "error": str(e)}
    return results


def collect_kospi():
    results = {}
    today = datetime.now().strftime("%Y%m%d")
    yesterday = (datetime.now() - timedelta(days=3)).strftime("%Y%m%d")  # 3일 여유

    for name, code in KOSPI_TICKERS.items():
        try:
            df = krx.get_market_ohlcv(yesterday, today, code)
            if df.empty:
                continue
            close = int(df["종가"].iloc[-1])
            prev  = int(df["종가"].iloc[-2]) if len(df) >= 2 else close
            results[name] = {
                "code":       code,
                "close":      close,
                "change_pct": _pct(close, prev),
            }
        except Exception as e:
            results[name] = {"code": code, "error": str(e)}
    return results


def collect_kospi_index():
    try:
        today = datetime.now().strftime("%Y%m%d")
        yesterday = (datetime.now() - timedelta(days=3)).strftime("%Y%m%d")
        df = krx.get_index_ohlcv(yesterday, today, "1028")  # KOSPI 지수
        if df.empty:
            return {}
        close = round(float(df["종가"].iloc[-1]), 2)
        prev  = round(float(df["종가"].iloc[-2]), 2) if len(df) >= 2 else close
        return {"코스피 지수": {"close": close, "change_pct": _pct(close, prev)}}
    except Exception as e:
        return {"코스피 지수": {"error": str(e)}}


# ── 메인 ──────────────────────────────────────────────────

def run():
    collected_at = datetime.now().isoformat()
    print(f"[{collected_at}] 시황 수집 시작")

    nasdaq = collect_nasdaq()
    kospi  = collect_kospi()
    kospi_idx = collect_kospi_index()

    payload = {
        "collected_at": collected_at,
        "nasdaq":       nasdaq,
        "kospi_index":  kospi_idx,
        "kospi":        kospi,
    }

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_file = OUTPUT_DIR / f"{date_str}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # 최신 파일도 덮어쓰기 (랜딩 페이지·대시보드용)
    latest = OUTPUT_DIR / "latest.json"
    with open(latest, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"  저장: {out_file}")
    return payload


if __name__ == "__main__":
    run()
