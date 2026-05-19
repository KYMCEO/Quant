#!/bin/bash

# ---------------------------------------------
# Auto Git Sync Script (Local Fallback)
# 이 스크립트는 Auto Sync 시스템의 역할을 로컬에서 수행합니다.
# ---------------------------------------------

echo "=========================================="
echo "🚀 [AutoSync] 시작: 변경 사항 검색 및 커밋 준비"
echo "=========================================="

# 1. 모든 변경된 파일을 스테이징 영역에 추가 (Add)
git add .
if [ $? -ne 0 ]; then
    echo "❌ [ERROR] git add 실패. 파일 시스템 접근 권한을 확인하세요."
    exit 1
fi

# 2. 커밋할 내용이 있는지 확인
STATUS=$(git status --porcelain)
if [[ -z "$STATUS" ]]; then
    echo "✅ [SUCCESS] 로컬 작업 디렉토리에 커밋할 변경 사항이 없습니다. Sync를 종료합니다."
    exit 0
fi

# 3. 임시 커밋 메시지를 생성하고 강제 커밋 (Commit)
COMMIT_MESSAGE="feat(sync): Auto Sync 스크립트를 통한 자동 동기화 반영"
git commit -m "$COMMIT_MESSAGE"

if [ $? -ne 0 ]; then
    echo "❌ [ERROR] git commit 실패. 이미 동일한 내용을 커밋했을 수 있습니다."
    exit 1
fi

# 4. 원격 저장소로 강제 푸시 (Push)
echo ""
echo "✨ [AutoSync] 최종 푸시를 시도합니다..."
git push origin main

if [ $? -ne 0 ]; then
    echo "🚨 [CRITICAL FAILURE] git push 실패! 인증 토큰 또는 권한을 확인해주세요."
else
    echo "✅ [SUCCESS] 모든 변경 사항이 원격 저장소(origin/main)에 성공적으로 동기화되었습니다!"
fi