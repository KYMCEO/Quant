#!/usr/bin/env python3
"""
AI Stock Factory — 시황 자동 스케줄러
매일 오전 9:05 (한국 시간 기준, 장 시작 직후) 자동 실행
"""

import time
import schedule
from collector import run as collect
from analyzer  import run as analyze


def daily_job():
    print("=" * 50)
    print("🕘 시황 자동 수집 시작")
    collect()
    analyze()
    print("✅ 완료")
    print("=" * 50)


# 매일 오전 9:05 실행
schedule.every().day.at("09:05").do(daily_job)

if __name__ == "__main__":
    print("📅 스케줄러 시작 — 매일 09:05 자동 실행")
    print("   지금 즉시 실행하려면 Ctrl+C 후 collector.py를 직접 실행하세요")
    while True:
        schedule.run_pending()
        time.sleep(30)
