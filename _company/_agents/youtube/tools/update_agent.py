#!/usr/bin/env python3
"""
에이전트 홈페이지 대시보드 업데이트 도구.
이 파일은 _company/_agents/developer/tools/ 에 위치하며,
상대 경로로 data.json 을 찾으므로 한글 경로 문제가 없습니다.

사용법:
  python update_agent.py <agent_id> <status> "<메시지>" [--revenue 금액] [--content-count N]

예시:
  python update_agent.py researcher done "삼성전자 분석 완료"
  python update_agent.py youtube active "트렌드 스나이핑 중" --content-count 1
  python update_agent.py business done "수익 집계 완료" --revenue 150000

agent_id: researcher, writer, youtube, designer, instagram, editor, business, secretary, developer
status:   active | done | idle | error
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

# 이 파일에서 4단계 상위 = 워크스페이스 루트 → developer/inhost/data.json
DATA_FILE = Path(__file__).resolve().parent / "../../../../developer/inhost/data.json"
MAX_FEED = 10

VALID_AGENTS = [
    "researcher", "writer", "youtube", "designer",
    "instagram", "editor", "business", "secretary", "developer"
]
VALID_STATUSES = ["active", "done", "idle", "error"]


def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("agent_id", choices=VALID_AGENTS)
    parser.add_argument("status", choices=VALID_STATUSES)
    parser.add_argument("message")
    parser.add_argument("--revenue", type=int, default=None)
    parser.add_argument("--content-count", type=int, default=None, dest="content_count")
    args = parser.parse_args()

    data = load_data()
    agent = data["agents"][args.agent_id]
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    agent["status"] = args.status
    agent["last_run"] = now
    agent["feed"].insert(0, {"time": now, "message": args.message, "status": args.status})
    agent["feed"] = agent["feed"][:MAX_FEED]

    if args.content_count:
        data["factory"]["content_today"] += args.content_count
    if args.revenue:
        data["factory"]["revenue_month"] += args.revenue

    data["factory"]["active_agents"] = sum(
        1 for a in data["agents"].values() if a["status"] == "active"
    )
    data["last_updated"] = now

    save_data(data)
    print(f"OK: {args.agent_id} -> {args.status}: {args.message}")


if __name__ == "__main__":
    main()
