import PyPDF2
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    PDF 파일에서 모든 텍스트를 추출해 하나의 문자열로 반환합니다.
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    text_chunks = []

    with pdf_path.open("rb") as f:
        reader = PyPDF2.PdfReader(f)

        for page_num, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text() or ""
            except Exception as e:
                print(f"[WARN] {page_num} 페이지 텍스트 추출 중 오류: {e}")
                page_text = ""

            text_chunks.append(page_text)

    return "\n".join(text_chunks)
