import re
from typing import List, Tuple


def detect_heading_lines(lines: List[str]) -> List[Tuple[int, str]]:
    """
    단순 규칙 기반으로 '제목/섹션'으로 보이는 줄을 찾아냅니다.
    반환: (line_number(1부터), line_text)
    """
    headings: List[Tuple[int, str]] = []

    # 정규식 패턴 예시:
    # 1. 서론 / 1.1 배경 / I. INTRO / 제1장 서론 등
    patterns = [
        r"^\d+(\.\d+)*\s+.+",                # 1. 제목 / 1.1 소제목
        r"^[IVXLC]+\.\s+.+",                 # I. INTRODUCTION
        r"^제\s*\d+\s*[장절편]\s+.+",        # 제 1 장 서론
        r"^(서론|결론|본론|참고문헌)\s*$",    # 대표적인 단일 섹션명
    ]

    compiled_patterns = [re.compile(p) for p in patterns]

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line:
            continue
        if len(line) < 3:
            continue
        if len(line) > 80:
            continue  # 너무 긴 줄은 본문으로 간주

        for pat in compiled_patterns:
            if pat.match(line):
                headings.append((idx, line))
                break

    return headings


def generate_toc(text: str) -> str:
    """
    전체 텍스트에서 목차(TOC)에 들어갈 만한 제목 후보들을 찾아
    사람이 보기 쉬운 문자열로 반환합니다.
    """
    lines = text.splitlines()
    heading_candidates = detect_heading_lines(lines)

    if not heading_candidates:
        return "자동으로 추출된 목차 후보가 없습니다."

    toc_lines = []
    toc_lines.append("자동 생성 목차(제목 후보):")
    toc_lines.append("-" * 40)

    for line_no, heading in heading_candidates:
        toc_lines.append(f"{line_no:>4}행: {heading}")

    return "\n".join(toc_lines)
