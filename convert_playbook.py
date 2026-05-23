"""
AI Stock Factory — 플레이북 PDF 변환기 (fpdf2 기반, 외부 라이브러리 불필요)
"""
import re
from pathlib import Path
from fpdf import FPDF

INPUT_MD   = Path("sessions/2026-05-23T10-00/playbook_draft.md")
OUTPUT_PDF = Path("data/products/playbook_v1.pdf")
OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)

# ── 색상 ──────────────────────────────────────────────────
BG        = (10,  25,  49)   # Deep Navy  #0A1931
CYAN      = (0,   255, 255)  # Electric Cyan #00FFFF
GOLD      = (240, 180, 41)   # Gold
WHITE     = (224, 224, 240)
MUTED     = (120, 120, 154)
DARK_CARD = (19,  19,  26)   # Surface


class Playbook(FPDF):
    def header(self):
        self.set_fill_color(*BG)
        self.rect(0, 0, 210, 297, "F")

    def footer(self):
        self.set_y(-15)
        self.set_font("Malgun", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 10, f"AI Stock Factory  |  Confidential  |  Page {self.page_no()}", align="C")

    def cover_page(self, title, subtitle, price):
        self.add_page()
        # 상단 Cyan 라인
        self.set_fill_color(*CYAN)
        self.rect(0, 0, 210, 4, "F")

        # 제목
        self.set_y(60)
        self.set_font("Malgun", "B", 28)
        self.set_text_color(*CYAN)
        self.multi_cell(0, 12, title, align="C")

        # 부제
        self.ln(6)
        self.set_font("Malgun", "", 13)
        self.set_text_color(*WHITE)
        self.multi_cell(0, 7, subtitle, align="C")

        # 가격 뱃지
        self.ln(20)
        self.set_font("Malgun", "B", 18)
        self.set_text_color(*GOLD)
        self.cell(0, 10, price, align="C")

        # 하단 브랜드
        self.set_y(-40)
        self.set_font("Malgun", "B", 10)
        self.set_text_color(*MUTED)
        self.cell(0, 6, "AI STOCK FACTORY", align="C")
        self.ln(5)
        self.set_font("Malgun", "", 9)
        self.cell(0, 5, "Global Regulatory Gap Analysis  |  2026", align="C")

    def _reset_x(self):
        self.set_x(self.l_margin)

    def chapter_title(self, text):
        self.ln(6)
        self.set_fill_color(*CYAN)
        self.rect(14, self.get_y(), 3, 10, "F")
        self.set_x(20)
        self.set_font("Malgun", "B", 14)
        self.set_text_color(*CYAN)
        self.multi_cell(176, 10, text)
        self._reset_x()
        self.set_draw_color(*CYAN)
        self.set_line_width(0.3)
        self.line(14, self.get_y(), 196, self.get_y())
        self.ln(4)
        self._reset_x()

    def section_title(self, text):
        self.ln(4)
        self.set_font("Malgun", "B", 11)
        self.set_text_color(*GOLD)
        self.multi_cell(182, 7, text)
        self.ln(1)
        self._reset_x()

    def body_text(self, text):
        self.set_font("Malgun", "", 10)
        self.set_text_color(*WHITE)
        self.multi_cell(182, 6, text)
        self.ln(1)
        self._reset_x()

    def bullet(self, text):
        self.set_font("Malgun", "", 10)
        self.set_x(18)
        self.set_text_color(*CYAN)
        self.cell(5, 6, "\x95")
        self.set_text_color(*WHITE)
        self.multi_cell(177, 6, text)
        self._reset_x()

    def highlight_box(self, text):
        self.set_fill_color(*DARK_CARD)
        self.set_draw_color(*CYAN)
        self.set_line_width(0.5)
        y = self.get_y()
        self.rect(14, y, 182, 14, "FD")
        self.set_xy(18, y + 3)
        self.set_font("Malgun", "B", 10)
        self.set_text_color(*CYAN)
        self.multi_cell(174, 6, text)
        self.ln(4)
        self._reset_x()


def clean(text):
    """마크다운 기호 및 이모지 제거"""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*",     r"\1", text)
    text = re.sub(r"`(.+?)`",       r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    # 이모지 제거 (Malgun Gothic 미지원 문자 방어)
    text = "".join(c for c in text if ord(c) < 0x10000)
    return text.strip()


def render_md(pdf, md_text):
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if line.startswith("# "):
            pdf.cover_page(
                clean(line[2:]),
                "미국·EU·아시아 전력 규제 격차가 만드는 2026 투자 기회",
                "$299 USD"
            )
        elif line.startswith("## "):
            pdf.add_page()
            pdf.chapter_title(clean(line[3:]))
        elif line.startswith("### "):
            pdf.section_title(clean(line[4:]))
        elif line.startswith("- ") or line.startswith("* "):
            pdf.bullet(clean(line[2:]))
        elif line.startswith("> "):
            pdf.highlight_box(clean(line[2:]))
        elif line.startswith("|"):
            # 테이블 — 헤더 행만 굵게, 나머지 일반
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.match(r"^[-: ]+$", c) for c in cells if c):
                i += 1
                continue
            pdf.set_font("Malgun", "", 9)
            pdf.set_text_color(*WHITE)
            col_w = 176 // max(len(cells), 1)
            is_header = lines[i-1].startswith("|") is False or (i+1 < len(lines) and re.match(r"^\|[-| :]+\|", lines[i+1]))
            if is_header:
                pdf.set_fill_color(*DARK_CARD)
                pdf.set_font("Malgun", "B", 9)
                pdf.set_text_color(*CYAN)
            for cell in cells:
                if cell:
                    pdf.cell(col_w, 7, clean(cell)[:30], border=1, fill=is_header)
            pdf.ln()
        elif line == "" or line == "---":
            pdf.ln(3)
        else:
            pdf.body_text(clean(line))

        i += 1


def main():
    md_text = INPUT_MD.read_text(encoding="utf-8")

    pdf = Playbook()
    pdf.add_font("Malgun",  "", r"C:\Windows\Fonts\malgun.ttf")
    pdf.add_font("Malgun",  "B", r"C:\Windows\Fonts\malgunbd.ttf")
    pdf.set_font("Malgun", size=10)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(14, 16, 14)

    render_md(pdf, md_text)

    pdf.output(str(OUTPUT_PDF))

    size_kb = OUTPUT_PDF.stat().st_size // 1024
    print(f"PDF 생성 완료: {OUTPUT_PDF}")
    print(f"크기: {size_kb} KB  |  페이지: {pdf.page}")


if __name__ == "__main__":
    main()
