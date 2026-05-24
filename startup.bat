@echo off
cd /d "c:\Users\pc\비즈니스 ai"

:: 시황 데이터 수집
start "" python developer/market/collector.py

:: 잠깐 대기 후 서버 실행
timeout /t 5 /nobreak >nul
start "" python developer/inhost/server.py

:: 스케줄러 (매일 09:05 자동 수집)
start "" python developer/market/scheduler.py

echo AI Stock Factory 서버 시작 완료 — http://localhost:8080
