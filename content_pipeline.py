import json
from typing import Dict, Any, List, Optional

# --- 1. 데이터 스키마 정의 (Schema Definition) ---

class ContentInputSchema:
    """
    [INPUT] 모든 플랫폼 재활용의 원본이 되는 표준화된 콘텐츠 구조.
    'Core Script'가 이 스키마를 따르도록 강제해야 합니다.
    """
    def __init__(self, title: str, topic_keywords: List[str], core_script_text: str, original_source: str):
        self.title = title  # 원본 콘텐츠 제목 (예: 'AI 규제 지뢰밭 분석')
        self.topic_keywords = topic_keywords # 핵심 주제 키워드 (예: ['규제', '데이터 주권', '전력 인프라'])
        self.core_script_text = core_script_text # 원본 스크립트 본문 (가장 길고 상세함)
        self.original_source = original_source # 출처/작성 에이전트

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            title=data.get("title", "No Title"),
            topic_keywords=data.get("keywords", []),
            core_script_text=data.get("script_text", ""),
            original_source=data.get("source", "Unknown")
        )

class RepurposedOutputSchema:
    """
    [OUTPUT] 각 플랫폼에 최적화되어 최종 사용될 콘텐츠 구조.
    'Repurpose' 함수들이 이 스키마를 채우게 됩니다.
    """
    def __init__(self, platform: str, caption: str, hashtags: List[str], schedule_suggestion: str, content_summary: str):
        self.platform = platform # IG Reel, YT Short, X Cardnews 등
        self.caption = caption # 플랫폼별 최적 길이의 캡션/설명글
        self.hashtags = hashtags # 필수 해시태그 세트 (최대 개수 제한)
        self.schedule_suggestion = schedule_suggestion # 분석 기반 최적 업로드 시간 및 요일
        self.content_summary = content_summary # 해당 플랫폼에 맞춰 재구성된 핵심 메시지

    def to_dict(self):
        return self.__dict__


# --- 2. 코어 파이프라인 로직 (Core Logic) ---

class ContentRepurposer:
    """
    핵심 콘텐츠 스크립트를 다양한 소셜 미디어 플랫폼 형식에 맞게 재활용하는 메인 엔진.
    """

    def __init__(self, core_script: ContentInputSchema):
        self.core_script = core_script
        print("✅ ContentRepurposer 초기화 완료. 핵심 스크립트 분석 시작...")

    # -------------------------
    # A. 플랫폼별 어댑터 함수들 (Adapters)
    # -------------------------

    def _extract_key_insight(self, script: str, keywords: List[str]) -> str:
        """
        [Utility] 핵심 스크립트와 키워드를 기반으로 가장 임팩트 있는 단 하나의 인사이트를 요약합니다.
        실제로는 LLM API 호출이 필요하지만, 여기서는 로직을 시뮬레이션합니다.
        """
        return f"[{keywords[0]} 리스크] {script[:100].replace('\\n', ' ')}... 핵심은 규제가 돈의 흐름을 바꾼다는 것입니다."

    def adapt_for_instagram(self) -> RepurposedOutputSchema:
        """
        Instagram Reel용 어댑터: 시각적 후킹과 짧고 간결한 액션 유도에 초점.
        캡션은 짧게, 내용은 '질문'이나 '위협 인지'로 시작해야 합니다.
        """
        summary = self._extract_key_insight(self.core_script.core_script_text, self.topic_keywords)
        caption = (
            f"🚨 멈춰! 지금 당신의 포트폴리오가 놓치고 있는 위험 신호가 있습니다.\n"
            f"{summary}\n\n"
            f"이 리스크를 해결할 '실행 매뉴얼'은 프로필 링크에서 확인하세요. 👇 #AI주식팩토리"
        )
        hashtags = ["#aiinvest", "#규제리스크", "주식꿀팁", "#financialfreedom"]
        schedule = self._suggest_optimal_schedule("Instagram Reel")
        return RepurposedOutputSchema(
            platform="Instagram Reel", 
            caption=caption, 
            hashtags=hashtags, 
            schedule_suggestion=schedule, 
            content_summary=f"🔥 [Reel] 시각적 위협 경고에 집중. 짧은 호흡으로 공포감 유발."
        )

    def adapt_for_youtube(self) -> RepurposedOutputSchema:
        """
        YouTube Short용 어댑터: 설명란과 제목을 통해 긴밀한 Funnel 구조를 유지해야 함.
        상세하게 내용을 요약하고, CTA를 명확히 제시합니다.
        """
        summary = self._extract_key_insight(self.core_script.core_script_text, self.topic_keywords)
        caption = (
            f"📚 [Full Analysis] {self.core_script.title}에 대한 심층 분석입니다.\n\n"
            f"규제 변화가 시장의 돈의 흐름을 어떻게 바꾸는지 10분짜리 영상에서 자세히 다뤘습니다.\n\n"
            f"💡 [핵심 요약]: {summary}\n\n"
            f"🔥 이 위험을 선제적으로 회피하려면, 댓글 상단 고정 링크를 확인하세요. (플레이북 구매 Funnel)"
        )
        hashtags = ["#ai주식", "#투자전략", "재테크꿀팁", "규제분석"]
        schedule = self._suggest_optimal_schedule("YouTube Short")
        return RepurposedOutputSchema(
            platform="YouTube Short", 
            caption=caption, 
            hashtags=hashtags, 
            schedule_suggestion=schedule, 
            content_summary=f"📊 [Short] 전문성/권위 강조. 설명란에 상세 CTA 및 Funnel 구조 배치."
        )

    def adapt_for_x(self) -> RepurposedOutputSchema:
        """
        X (Twitter) Cardnews용 어댑터: 초단문, 질문형 후킹과 즉각적인 행동을 유도해야 함.
        가장 간결하고 충격적인 문구만 남기고, 해시태그로 트렌드를 잡습니다.
        """
        summary = self._extract_key_insight(self.core_script.core_script_text, self.topic_keywords)
        # X는 텍스트 자체가 핵심입니다. 질문으로 끝냅니다.
        caption = f"⚡️ 경고: 당신이 모르는 글로벌 규제 변화가 주식 섹터를 무너뜨립니다.\n\n👉 지금 가장 위험한 곳은? [핵심 키워드] 분야의 데이터 주권 리스크입니다.\n\n자세한 Playbook은 프로필 링크에서 바로 확인하세요. #AI팩토리"
        hashtags = ["#주식경고", "#데이터주권", "TechRisk", "Investment"]
        schedule = self._suggest_optimal_schedule("X/Twitter")
        return RepurposedOutputSchema(
            platform="X Cardnews", 
            caption=caption, 
            hashtags=hashtags, 
            schedule_suggestion=schedule, 
            content_summary=f"🎯 [X] 최대의 임팩트와 즉각적인 행동 유도. 짧고 강력한 메시지 최적화."
        )

    # -------------------------
    # B. 보조/공통 로직 (Utility)
    # -------------------------

    def _suggest_optimal_schedule(self, platform: str) -> str:
        """
        가상의 데이터 기반으로 플랫폼별 최적 업로드 시간을 제안하는 함수입니다.
        실제로는 A/B 테스트 로그와 사용자 활동 데이터를 분석해야 합니다.
        """
        if "Instagram" in platform:
            return "평일 점심시간 (12:00 KST) 또는 저녁 피크 시간 (20:00 KST)"
        elif "YouTube" in platform:
            return "주말 오전 10시 KST (가장 많은 시간을 확보하는 시간대)"
        elif "X/Twitter" in platform:
            # 트래픽이 높은 시간에 짧게 여러 번 분산 배치하는 것이 유리합니다.
            return "평일 출퇴근 시간(07:30, 18:00 KST)에 세션별로 배포 권장."
        else:
            return "데이터 부족 — 수동 최적화 필요"

    def repurpose_all_platforms(self) -> Dict[str, RepurposedOutputSchema]:
        """
        모든 플랫폼 어댑터를 순차적으로 호출하여 최종 결과 딕셔너리를 반환합니다.
        """
        results = {}
        print("\n⚙️ [Repurpose] 모든 플랫폼에 대한 적응 작업을 실행합니다...")
        try:
            # 각 플랫폼별로 독립적인 프로세스처럼 처리합니다.
            results['instagram'] = self.adapt_for_instagram()
            results['youtube'] = self.adapt_for_youtube()
            results['x'] = self.adapt_for_x()
        except Exception as e:
            print(f"🚨 [ERROR] 재활용 과정 중 예외 발생: {e}")
            # 오류가 나면 원본 스크립트의 구조적 문제를 의심해야 합니다.
            raise

        return results


# --- 3. 테스트 실행 블록 (Testing Block) ---

if __name__ == "__main__":
    print("==================================================")
    print("          🚀 Content Repurposing Pipeline Test")
    print("==================================================")

    # [테스트 입력 데이터] 가상의 '규제 격차' 숏폼 원본 스크립트 데이터를 생성합니다.
    CORE_SCRIPT_DATA = {
        "title": "글로벌 규제 지뢰밭: AI 주식의 숨겨진 위험",
        "keywords": ["데이터 주권", "전력 인프라 리스크", "공급망/규제"],
        # 이 스크립트는 실제 7일치 중 가장 대표적인 내용으로 가정합니다.
        "script_text": (
            "최근 AI 섹터 투자의 핵심은 기술 자체보다 '어디서, 어떻게' 데이터를 처리할 수 있는지에 달려있습니다.\n"
            "특히 미국과 EU의 데이터 주권법(Data Sovereignty Law) 강화는 기업들의 인프라 구축 비용을 폭증시키고 있습니다. "
            "\n\n전력 인프라 리스크도 무시할 수 없습니다. AI 컴퓨팅은 전기를 엄청나게 먹거든요. 이 부분이 병목이 되면, 아무리 좋은 칩도 가동되지 못합니다.\n"
            "\n\n결론적으로, 단순히 기술력이 아니라 '규제 준수'와 '안정적 인프라 확보 능력' 자체가 가장 중요한 투자 기준점이 되었습니다. 이것이 바로 우리가 놓쳐서는 안 될 규제 격차 플레이북의 핵심입니다."
        ),
        "source": "AI Stock Factory (2026-05-23)"
    }

    # 1. 스키마를 이용해 객체화 및 초기 검증
    try:
        input_script = ContentInputSchema.from_dict(CORE_SCRIPT_DATA)
        print("\n✅ [Validation] Input Schema 유효성 검사 통과.")
    except Exception as e:
        print(f"❌ [FATAL ERROR] 입력 데이터 스키마 오류 발생: {e}")
        exit()

    # 2. 파이프라인 실행 및 재활용
    repurposer = ContentRepurposer(input_script)
    try:
        repurposed_outputs = repurposer.repurpose_all_platforms()

        print("\n==============================================")
        print("✨ [SUCCESS] 모든 플랫폼 콘텐츠 재활용 완료! ✨")
        print("==============================================")

        # 3. 결과 구조화 출력 (검증 용이하도록)
        for platform, output in repurposed_outputs.items():
            print(f"\n--- [{platform}] ---")
            print(f"📝 Summary: {output.content_summary}")
            print(f"⏰ Suggestion: {output.schedule_suggestion}")
            print("\n[Caption/Body Preview]")
            # 출력 시 보기 좋게 줄 바꿈을 유지하며 출력합니다.
            print(output.caption.replace('\n', '\n')) 
            print("\n[Hashtags]: " + ", ".join(output.hashtags))

    except Exception as e:
        print(f"\n❌ [FAILURE] 파이프라인 실행 실패. 원본 스크립트 또는 로직 재검토 필요: {e}")