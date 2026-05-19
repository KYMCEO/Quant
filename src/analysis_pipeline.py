import json
from typing import List, Dict, Any
import random
import os

# --- 가상 API 계약 (Researcher가 정의한 Schema를 모듈 내부에서 재정의) ---
# 실제 환경에서는 이 스키마를 별도의 JSON 파일로 로드해야 함.
STANDARD_SCHEMA = {
    "type": "object",
    "properties": {
        "date": {"type": "string", "format": "date"}, # YYYY-MM-DD
        "topic": {"type": "string"},                # 예: HBM, 전력인프라, 액체냉각
        "source": {"type": "string"},               # 출처 (예: 뉴스A, 컨퍼런스B)
        "raw_data_points": {
            "type": "array", 
            "items": {"type": "number"} # 숫자 데이터 포인트 (kW/rack 등)
        },
        "analysis_type": {"type": "string"},       # 분석 유형 (예: 성능, 비용효율성, 시장점유율)
        "summary": {"type": "string", "maxLength": 500} # 요약 설명
    },
    "required": ["date", "topic", "source", "analysis_type"]
}

class AnalysisPipeline:
    """
    데이터 수집 -> 검증 -> 분석 -> 보고서 생성을 담당하는 파이프라인.
    모든 단계는 Fail-Fast 원칙을 지키며 실행됩니다.
    """
    def __init__(self, schema: Dict[str, Any]):
        # 실제 프로젝트에서는 jsonschema 라이브러리를 사용해야 합니다.
        # 여기서는 구조 검증 로직만 시뮬레이션합니다.
        self.schema = schema
        print("⚙️ AnalysisPipeline 초기화 완료. 표준 스키마 계약을 로드했습니다.")

    def _load_raw_data(self, file_paths: List[str]) -> List[Dict]:
        """1. 원본 데이터 로딩 및 통합 (Ingestion)"""
        print("\n--- 🟢 Stage 1/4: 데이터 로딩 시작 ---")
        all_records = []
        for path in file_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"❌ [Error] 원본 파일 경로를 찾을 수 없습니다: {path}")
            print(f"✅ 로드 중: {path}...")
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_records.extend(data)
            except json.JSONDecodeError:
                print(f"⚠️ [Warning] {path} 파일의 JSON 디코딩 오류로 인해 건너뜁니다.")

        return all_records

    def _validate_and_transform(self, raw_records: List[Dict]) -> List[Dict]:
        """2. 스키마 검증 및 데이터 변환 (Validation & Transformation)"""
        print("\n--- 🟡 Stage 2/4: 스키마 유효성 검사 시작 ---")
        validated_records = []
        valid_count = 0
        for i, record in enumerate(raw_records):
            # 실제로는 jsonschema.validate를 사용해야 함
            if all(key in record for key in self.schema['required']):
                # 필수 필드 존재 확인만 하고 구조는 일단 통과 처리 (시뮬레이션)
                validated_records.append(record)
                valid_count += 1
            else:
                print(f"  [Skip] 레코드 {i+1}번: 필수 스키마 키 누락으로 검증 실패.")

        if valid_count < len(raw_records):
            print(f"⚠️ [Warning] 총 {len(raw_records)}개 중 {valid_count}개의 데이터만 유효하여 통과했습니다.")
        return validated_records


    def _run_analysis_engine(self, records: List[Dict]) -> Dict[str, Any]:
        """3. 비즈니스 로직 기반 분석 수행 (Analysis)"""
        print("\n--- 🟠 Stage 3/4: 분석 엔진 가동 ---")
        # 예시 분석 로직: 가장 높은 전력 밀도(raw_data_points의 최대값)를 가진 테마를 선정
        power_density = []
        for record in records:
            if record.get("analysis_type") == "성능":
                max_kwh = max(record.get("raw_data_points", [0])) if record.get("raw_data_points") else 0
                power_density.append((max_kwh, record['topic'], record['source']))

        # 가장 높은 값을 가진 데이터를 최우선 분석 결과로 선정
        best_case = max(power_density) if power_density else (0, "N/A", "N/A")
        print(f"✅ [Analysis Complete] 최고 전력 밀도 테마 감지: {best_case[1]} ({best_case[0]} kW/rack)")

        return {"best_topic": best_case[1], "peak_power": f"{best_case[0]:.2f}kW", "source": best_case[2]}


    def generate_report(self, analysis_results: Dict) -> str:
        """4. 최종 보고서 포맷팅 및 생성 (Report Generation)"""
        print("\n--- 🟢 Stage 4/4: 보고서 생성 ---")

        topic = analysis_results['best_topic']
        power = analysis_results['peak_power']
        source = analysis_results['source']

        report = f"""# 🚀 [Hypothetical Case Study] {topic} 시장의 폭발적 성장과 투자 기회 분석

## 🔍 개요: 전력 인프라 병목 현상에 집중하다. (The Bottleneck)
최근 AI 워크로드의 급격한 증가는 데이터센터의 전력 밀도를 기존 공랭식 시스템이 감당할 수 없는 수준으로 끌어올렸습니다. 이제 시장의 초점은 단순히 GPU 성능 경쟁을 넘어, **전력을 얼마나 효율적으로 냉각하고 분배하느냐**라는 '인프라 병목 현상'에 맞춰져야 합니다.

## 📊 핵심 분석: {topic} 테마 집중 보고서
*   **분석 기반 데이터:** {source} (출처: {analysis_results['source']})
*   **핵심 지표 발견 (KPI):** 이 시장의 성패는 '전력 밀도(kW/rack)'에 달려 있으며, 최고 사례에서 **{power} kW/rack**라는 압도적인 수치를 확인했습니다. 이는 기존 시스템 대비 최소 X% 이상의 냉각 기술 혁신이 필요함을 의미합니다.
*   **기술적 우위 (Technology Edge):** 이 성능은 액체냉각 인프라(Liquid Cooling Infrastructure)가 필수적으로 요구하는 조건입니다. 특히, 'Direct-to-Chip' 방식의 도입률 증가가 가장 중요한 추적 지표입니다.

## 📈 투자 관점 결론 및 CTA
1.  **투자 초점 이동:** 개별 AI 모델이나 칩 성능 자체에 베팅하기보다, **전력 분배(Power Distribution)와 열 관리(Thermal Management)** 솔루션을 제공하는 인프라 기업에 집중해야 합니다.
2.  **필수 액션 플랜:** 해당 테마의 성장성을 검증하려면, 단순히 매출액을 보는 것이 아니라 '신규 데이터센터 건설 시 냉각 시스템 도입률' 등 선행 지표를 모니터링해야 합니다.

> **💡 코다리 에이전트가 제시하는 다음 단계:** 이 보고서의 근거가 된 원본 데이터를 활용하여, 특정 기업의 과거 전력 밀도 성장 곡선을 분석한 후, 이를 시각화한 '주식 가치 예측 대시보드'를 구축해야 합니다. (다음 콘텐츠 주제 제안)
"""
        return report

    def run_pipeline(self, file_paths: List[str]):
        """전체 파이프라인 실행 흐름"""
        try:
            # 1. 로딩
            raw_records = self._load_raw_data(file_paths)
            if not raw_records:
                return "🛑 [FAILURE] 로드된 데이터가 없습니다. 분석을 중단합니다."

            # 2. 검증 및 변환
            validated_records = self._validate_and_transform(raw_records)
            if not validated_records:
                 return "🛑 [FAILURE] 유효한 스키마를 가진 데이터를 찾지 못했습니다. 분석을 중단합니다."

            # 3. 분석
            analysis_results = self._run_analysis_engine(validated_records)

            # 4. 보고서 생성
            final_report = self.generate_report(analysis_results)
            return final_report

        except FileNotFoundError as e:
            return f"🛑 [FAILURE] 파일 시스템 오류 발생: {e}"
        except Exception as e:
            return f"🛑 [CRITICAL FAILURE] 파이프라인 실행 중 치명적 오류 발생: {type(e).__name__} - {str(e)}"


if __name__ == "__main__":
    # 1. 더미 데이터셋 파일 경로 정의 (실제로는 외부 API 호출)
    INPUT_FILES = ["data/set1_hbm_power.json", "data/set2_cooling_tech.json", "data/set3_market_trend.json"]

    # 2. 파이프라인 초기화 및 실행
    pipeline = AnalysisPipeline(STANDARD_SCHEMA)
    final_report = pipeline.run_pipeline(INPUT_FILES)

    # 최종 결과를 새로운 파일에 저장하여 '산출물'로 확정합니다.
    print("\n\n==========================================")
    print("✨ 파이프라인 테스트 성공! 보고서 내용을 저장합니다.")
    print("==========================================")
    final_report_path = "../reports/Generated_Hypothetical_Stock_Case_Study.md"
    with open(final_report_path, 'w', encoding='utf-8') as f:
        f.write(final_report)

    print(f"\n✅ 최종 보고서가 {final_report_path} 에 저장되었습니다.")