import markdown
from weasyprint import HTML, CSS
import os

# --- 설정 상수 ---
INPUT_MD = "sessions/2026-05-23T10-00/playbook_draft.md"
OUTPUT_PDF = "data/products/playbook_v1.pdf"
BACKGROUND_COLOR = "#0A1931" # Deep Navy
ACCENT_COLOR = "#00FFFF"     # Electric Cyan

def create_custom_css() -> str:
    """지정된 브랜드 색상을 적용하는 CSS 문자열을 생성합니다."""
    return f"""
    @page {{
        size: A4;
        margin: 2cm;
    }}
    body {{
        background-color: {BACKGROUND_COLOR}; /* Deep Navy 배경 */
        color: #E0FFFF; /* 밝은 Cyan 계열의 기본 텍스트 색상 */
        font-family: 'Arial', sans-serif;
        padding: 20px;
    }}
    h1, h2, h3 {{
        color: {ACCENT_COLOR} !important; /* 제목 강조색 적용 */
        border-bottom: 2px solid {ACCENT_COLOR};
        padding-bottom: 5px;
        margin-top: 40px;
    }}
    pre, code {{
        background-color: #1a3658; /* 코드 블록 배경 */
        color: {ACCENT_COLOR} !important;
        padding: 10px;
        border-radius: 5px;
        display: block;
        overflow-x: auto;
    }}
    blockquote {{
        background-color: #1a3658; /* 인용구 배경 */
        border-left: 5px solid {ACCENT_COLOR};
        padding: 10px 20px;
        margin: 20px 0;
        font-style: italic;
    }}
    /* 표 스타일링 (Table Styling) */
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }}
    th, td {{
        padding: 10px;
        text-align: left;
        border: 1px solid #3a5e8d; /* 어두운 테두리 */
    }}
    th {{
        background-color: {ACCENT_COLOR};
        color: {BACKGROUND_COLOR} !important; /* 제목 배경은 Cyan, 글자는 어둠 */
    }}
    """

def convert_md_to_pdf(input_path: str, output_path: str):
    """마크다운 파일을 읽어 CSS 스타일을 적용한 후 PDF로 변환합니다."""
    print("--- [Step 1/3] 마크다운 파일 로드 및 HTML 변환 시작 ---")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"입력 마크다운 파일을 찾을 수 없습니다: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 1. Markdown to HTML 변환
    html_fragment = markdown.markdown(md_content)

    # 2. 전체 문서 구조화 및 CSS 적용을 위한 HTML 생성
    css = create_custom_css()
    full_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8" /><title>플레이북 보고서</title><style>{css}</style></head><body>{html_fragment}</body></html>"""

    print("--- [Step 2/3] CSS 스타일 적용 및 PDF 생성 시작 (weasyprint 사용) ---")
    try:
        # weasyprint를 사용하여 HTML을 PDF로 변환
        HTML(string=full_html).write_pdf(output_path, stylesheets=[CSS(string=css)])
        print(f"✅ 성공적으로 PDF 파일이 생성되었습니다: {output_path}")
    except Exception as e:
        print(f"❌ PDF 생성 중 오류가 발생했습니다. 환경 설정을 확인하세요: {e}")
        raise

if __name__ == "__main__":
    try:
        convert_md_to_pdf(INPUT_MD, OUTPUT_PDF)
    except FileNotFoundError as e:
        print(f"⚠️ 스크립트 실행 실패: {e}")