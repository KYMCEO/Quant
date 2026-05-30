import json
from typing import Dict, Any, List
# 가상의 외부 라이브러리 임포트 (실제 구현 시 필요)
# from jsonschema import validate, ValidationError

class ContentPipelineProcessor:
    """
    자동화된 주식 콘텐츠 변환 및 검증 파이프라인 핵심 로직.
    JSON 스키마 유효성 검사 -> Hex 기반 렌더링 -> 플랫폼 분기 처리를 담당합니다.
    """
    def __init__(self, schema_path: str, design_spec_path: str):
        """
        초기화 시 필요한 외부 리소스를 로드하고 구조적 무결성을 확인합니다.
        :param schema_path: 통합 메타데이터 JSON 스키마 파일 경로.
        :param design_spec_path: 마스터 디자인 시스템 사양서 파일 경로.
        """
        print(f"[INFO] Processor Initializing...")
        self.schema = self._load_json_file(schema_path)
        self.design_spec = self._load_json_file(design_spec_path)

        if not self.schema or not self.design_spec:
            raise FileNotFoundError("필수 스키마 또는 디자인 사양 파일을 로드할 수 없습니다.")
        
        print("[SUCCESS] Schema and Design Spec loaded successfully.")

    def _load_json_file(self, path: str) -> Dict[str, Any] | None:
        """JSON 파일에서 데이터를 안전하게 읽어옵니다."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] File not found at {path}")
            return None
        except json.JSONDecodeError:
            print(f"[CRITICAL ERROR] Invalid JSON format in {path}")
            return None

    def validate_data(self, raw_data: Dict[str, Any]) -> bool:
        """
        1. JSON 스키마 유효성 검사를 수행합니다. 
        모든 입력 데이터가 정의된 구조를 따르는지 확인하는 가장 중요한 단계입니다.
        """
        print("\n--- [STAGE 1] Running Schema Validation ---")
        # 실제 환경에서는 jsonschema 라이브러리를 사용해야 합니다.
        try:
            # 예시 검증 로직 (실제 스키마와 매핑 필요)
            if 'analysis_type' not in raw_data or isinstance(raw_data['analysis_type'], str):
                 raise TypeError("Metadata must contain a list of analysis types.")

            print("[VALIDATION SUCCESS] Data structure conforms to the schema.")
            return True
        except (TypeError, KeyError) as e:
            print(f"[!!! VALIDATION FAILURE !!!] Detected structural error: {e}")
            return False

    def process_content(self, raw_data: Dict[str, Any]) -> str:
        """
        메타데이터를 받아 전체 파이프라인을 실행하고 최종 아웃풋 문자열을 반환합니다.
        """
        if not self.validate_data(raw_data):
            return "🚨 Validation Failed. Cannot proceed with content generation."

        # 다음 단계: 렌더링 및 플랫폼 분기 처리를 호출
        renderer = ContentRenderer(self.design_spec)
        output = renderer.render_for_platform(raw_data, platform="YouTube") # 기본값으로 YouTube 지정
        return output

# --- 가상 더미 파일 경로 설정 (실제 스키마가 없으므로 임시 경로 사용) ---
SCHEMA_PATH = "c:\\Users\\pc\\비즈니스 ai\\_company\\agents\\developer\\content_pipeline\\metadata.schema.json"
DESIGN_SPEC_PATH = "c:\\Users\\pc\\비즈니스 ai\\_company\\agents\\developer\\content_pipeline\\design_spec.json"

if __name__ == "__main__":
    # 테스트용 더미 데이터 (실제 JSON 스키마를 통과할 수 있는 구조)
    dummy_data = {
        "title": "HBM 규제 격차 분석: 미국 vs EU",
        "date": "2026-05-31",
        "metadata": [
            {"topic": "AI 컴퓨팅 능력 통제", "analysis_type": ["Regulatory Gap", "Supply Chain"]},
            {"topic": "정책 면역 점수 변화", "analysis_type": ["Policy Immunity Score"]}
        ],
        "raw_data_points": [{"key": "US Policy", "value": 0.8}, {"key": "EU Policy", "value": 0.4}]
    }

    try:
        processor = ContentPipelineProcessor(SCHEMA_PATH, DESIGN_SPEC_PATH)
        final_output = processor.process_content(dummy_data)
        print("\n==============================================")
        print("✅ FINAL GENERATED CONTENT OUTPUT (Mock):\n", final_output[:500] + "...")
    except FileNotFoundError as e:
        print(f"\n[FATAL] 초기화 실패: {e}")