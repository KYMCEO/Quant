#!/usr/bin/env python3
"""
에이전트가 작업 완료 후 호출하는 상태 업데이트 스크립트.

사용법:
  python update_agent.py <agent_id> <status> "<메시지>" [--revenue 금액] [--content-count N]

예시:
  python update_agent.py researcher active "삼성전자 2Q 실적 분석 완료"
  python update_agent.py youtube active "오늘 트렌드 키워드 5개 추출" --content-count 1
  python update_agent.py business active "이번 달 수익 집계" --revenue 150000

agent_id 목록:
  researcher, writer, youtube, designer, instagram, editor, business, secretary, developer

status:
  active  — 작업 중
  done    — 작업 완료
  idle    — 대기 중
  error   — 오류 발생
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data.json"
MAX_FEED = 10  # 에이전트당 피드 최대 보관 수

VALID_AGENTS = [
    "researcher", "writer", "youtube", "designer",
    "instagram", "editor", "business", "secretary", "developer"
]

VALID_STATUSES = ["active", "done", "idle", "error"]


def load_data() -> dict:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description="에이전트 상태 업데이트")
    parser.add_argument("agent_id", choices=VALID_AGENTS, help="에이전트 ID")
    parser.add_argument("status", choices=VALID_STATUSES, help="상태")
    parser.add_argument("message", help="작업 내용 메시지")
    parser.add_argument("--revenue", type=int, default=None, help="수익 금액 (원)")
    parser.add_argument("--content-count", type=int, default=None, dest="content_count",
                        help="생성된 콘텐츠 수")
    args = parser.parse_args()

    data = load_data()
    agent = data["agents"][args.agent_id]
    now = now_iso()

    # 에이전트 상태 업데이트
    agent["status"] = args.status
    agent["last_run"] = now

    # 피드에 최신 항목 추가 (최대 MAX_FEED 개 유지)
    feed_item = {"time": now, "message": args.message, "status": args.status}
    agent["feed"].insert(0, feed_item)
    agent["feed"] = agent["feed"][:MAX_FEED]

    # 팩토리 통계 업데이트
    if args.content_count:
        data["factory"]["content_today"] += args.content_count

    if args.revenue:
        data["factory"]["revenue_month"] += args.revenue

    # 활성 에이전트 수 재계산
    data["factory"]["active_agents"] = sum(
        1 for a in data["agents"].values() if a["status"] == "active"
    )

    # 전체 last_updated 갱신
    data["last_updated"] = now

    save_data(data)
    msg = f"[{now}] {agent['name']} -> {args.status}: {args.message}"
    print(msg.encode("utf-8", errors="replace").decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
