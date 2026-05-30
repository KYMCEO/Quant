import json
from typing import Dict, Any

class ContentRenderer:
    """
    마스터 디자인 시스템 사양을 기반으로 텍스트 데이터를 시각적 레이아웃(Hex 코드)에 맞춰 변환합니다.
    YouTube용 상세 보고서 HTML와 Instagram용 캐러셀 슬라이드 JSON/HTML로 분기 처리하는 역할을 합니다.
    """
    def __init__(self, design_spec: Dict[str, Any]):
        if not design_spec or 'color' not in design_spec:
            raise ValueError("Design Spec must contain color palette.")
        
        # 디자인 사양을 메모리에 로드하여 접근성을 높입니다.
        self.primary_bg = design_spec['color']['background']  # Deep Navy #0A1931 가정
        self.accent_red = design_spec['color']['warning']    # Red/Danger
        self.accent_cyan = design_spec['color']['flow']     # Electric Cyan #00FFFF

    def _apply_style(self, element: str) -> str:
        """주어진 요소에 Hex 코드를 기반으로 스타일링 클래스를 강제 적용합니다."""
        return f'style="background-color: {self.primary_bg}; color: white; border-left: 5px solid {self.accent_cyan};"'

    def render_for_platform(self, data: Dict[str, Any], platform: str) -> str:
        """
        입력된 데이터를 플랫폼별 요구사항에 맞게 변환하고 HTML 구조를 생성합니다.
        """
        print(f"\n--- [STAGE 2] Rendering Content for {platform} ---")
        
        if platform == "YouTube":
            # YouTube는 심층 보고서가 필요하므로, 긴 형식의 HTML을 목표로 합니다.
            html_output = self._render_youtube_report(data)
        elif platform == "Instagram":
            # Instagram은 시각적 임팩트와 CTA가 중요하므로, 슬라이드 배열 JSON/HTML을 목표로 합니다.
            return self._render_instagram_carousel(data)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        print("[RENDER SUCCESS] Platform-specific rendering completed.")
        return html_output


    def _render_youtube_report(self, data: Dict[str, Any]) -> str:
        """YouTube 심층 보고서 포맷 (긴 HTML/Markdown)을 생성합니다."""
        header = f'<div class="{self._apply_style("")}"><h1>{data.get("title", "Untitled Report")}</h1><p>Date: {data.get("date")}</p></div>'
        
        sections = []
        for meta in data.get('metadata', []):
            topic = meta['topic']
            analysis_type = ", ".join(meta['analysis_type'])
            section = f'<h2 style="color: {self.accent_cyan};">{topic} ({analysis_type})</h2><p>...</p>' # 실제 분석 내용을 여기에 삽입
            sections.append(section)
        
        return header + "\n" + "<hr>\n".join(sections)

    def _render_instagram_carousel(self, data: Dict[str, Any]) -> str:
        """Instagram 캐러셀 (슬라이드별 JSON/HTML)을 생성합니다."""
        # 첫 슬라이드는 반드시 후킹 문구와 CTA가 포함되어야 함.
        hook = f"🔥 {data.get('title')}에 대한 충격적인 진실! (Swipe ➡️)"
        slide_1_content = f'<div style="background-color: #FF6600; color: white;">{hook}</div>'
        
        # 나머지 슬라이드는 문제점(Problem) - 해결책(Solution) 구조를 따름.
        slides = [
            f"<div style='border-bottom: 1px solid {self.primary_bg}; padding: 20px;'><h3>[문제] 규제 격차의 위험성</h3><p>데이터 기반 분석 필요</p></div>"
        ] + [
            f"<div style='background-color: #A3D9FF; color: black; padding: 20px;'><h3>[해결책] Policy Immunity Score 적용 방안</h3><p>구체적 로드맵 제시.</p></div>"
        ]
        return f"""
        =============================================
        ✨ INSTAGRAM CAROUSEL OUTPUT (JSON/HTML Mock) ✨
        ---------------------------------------------
        Slide 1: {slide_1_content}
        {chr(10)}
        Slide 2: {slides[0]}
        {chr(10)}
        Slide 3: {slides[1]}
        =============================================
        """