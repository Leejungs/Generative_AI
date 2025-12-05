import argparse
from pathlib import Path

import nltk

from src.extractor import extract_text_from_pdf
from src.summarizer import summarize_text
from src.toc_generator import generate_toc
from src.utils import ensure_output_dir


def setup_nltk():
    """
    NLTK에서 필요한 리소스를 자동으로 다운로드합니다.
    (이미 설치되어 있으면 그냥 넘어감)
    """
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        print("[INFO] NLTK punkt 리소스를 다운로드합니다...")
        nltk.download("punkt")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PDF 문서 요약 + 자동 목차 생성기 (미니 프로젝트)"
    )
    parser.add_argument(
        "--input_path",
        type=str,
        required=True,
        help="입력 PDF 파일 경로",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="outputs",
        help="요약/목차 결과를 저장할 디렉터리 (기본값: outputs)",
    )
    parser.add_argument(
        "--summary_only",
        action="store_true",
        help="요약만 생성할 경우 사용",
    )
    parser.add_argument(
        "--toc_only",
        action="store_true",
        help="목차만 생성할 경우 사용",
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="ko",
        choices=["ko", "en"],
        help="문서 언어 설정 (ko / en). 현재 버전에서는 크게 영향을 주지 않지만 추후 확장용.",
    )

    return parser.parse_args()


def main():
    setup_nltk()
    args = parse_args()

    pdf_path = args.input_path
    output_dir = ensure_output_dir(args.output_dir)

    print(f"[INFO] PDF 텍스트 추출 중... ({pdf_path})")
    full_text = extract_text_from_pdf(pdf_path)
    if not full_text.strip():
        print("[ERROR] PDF에서 텍스트를 추출하지 못했습니다.")
        return

    # 요약 생성
    summary_text = ""
    toc_text = ""

    if not args.toc_only:
        print("[INFO] 요약 생성 중...")
        summary_text = summarize_text(full_text, ratio=0.2, max_sentences=12)
        summary_file = output_dir / "summary.txt"
        summary_file.write_text(summary_text, encoding="utf-8")
        print(f"[INFO] 요약 결과 저장 완료: {summary_file}")

    if not args.summary_only:
        print("[INFO] 자동 목차(제목 후보) 생성 중...")
        toc_text = generate_toc(full_text)
        toc_file = output_dir / "toc.txt"
        toc_file.write_text(toc_text, encoding="utf-8")
        print(f"[INFO] 목차 후보 결과 저장 완료: {toc_file}")

    print("[DONE] 작업이 완료되었습니다.")


if __name__ == "__main__":
    main()
