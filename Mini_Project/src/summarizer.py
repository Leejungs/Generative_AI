from typing import List
import re
import math

import nltk

# 한국어/영어 섞여 있는 상황을 고려해서,
# 문장 분리는 간단한 규칙 + NLTK(영어 위주) 혼합 사용
def split_sentences(text: str) -> List[str]:
    """
    텍스트를 문장 단위로 대략적으로 분리합니다.
    한국어/영어 혼합을 가정하여 간단 규칙 기반으로 처리.
    """
    # 먼저 줄단위로 자르고
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    temp_text = " ".join(lines)

    # 마침표/물음표/느낌표 기준 1차 분리
    rough_sentences = re.split(r"(?<=[\.!?])\s+", temp_text)

    # 너무 짧은 문장은 앞 문장에 붙이거나 제거
    sentences: List[str] = []
    buffer = ""
    for s in rough_sentences:
        s = s.strip()
        if not s:
            continue
        if len(s) < 10:
            # 이전 버퍼에 붙이기
            buffer = f"{buffer} {s}".strip()
        else:
            if buffer:
                sentences.append(buffer)
                buffer = ""
            sentences.append(s)

    if buffer:
        sentences.append(buffer)

    return sentences


def build_frequency_table(text: str) -> dict:
    """
    매우 단순한 단어 빈도 기반 요약을 위한 frequency table 생성.
    (실제 프로젝트에서는 transformers 기반 요약 모델로 교체 가능)
    """
    # 알파벳/숫자/한글만 남기고 나머지는 공백 처리
    cleaned = re.sub(r"[^0-9A-Za-z가-힣\s]", " ", text)
    tokens = cleaned.lower().split()

    freq_table = {}
    for word in tokens:
        if len(word) <= 1:
            continue
        freq_table[word] = freq_table.get(word, 0) + 1

    if not freq_table:
        return {}

    # 정규화
    max_freq = max(freq_table.values())
    for word in list(freq_table.keys()):
        freq_table[word] = freq_table[word] / max_freq

    return freq_table


def score_sentences(sentences: List[str], freq_table: dict) -> dict:
    """
    각 문장에 대해 단어 점수의 합으로 문장 점수를 계산합니다.
    """
    sentence_scores = {}
    for sent in sentences:
        # 문장을 소문자 + 특수문자 제거
        cleaned_sent = re.sub(r"[^0-9A-Za-z가-힣\s]", " ", sent.lower())
        words = cleaned_sent.split()
        if not words:
            continue

        score = 0.0
        for w in words:
            score += freq_table.get(w, 0.0)

        if score <= 0:
            continue

        sentence_scores[sent] = score

    return sentence_scores


def summarize_text(text: str, ratio: float = 0.2, max_sentences: int = 10) -> str:
    """
    매우 단순한 extractive summarization.
    - ratio: 전체 문장 수 대비 요약에 포함할 비율
    - max_sentences: 최대 문장 수 제한

    TODO: 실제 프로젝트에서는 KoBART / Pegasus / BART 등
          Hugging Face 요약 모델로 교체할 수 있음.
    """
    if not text.strip():
        return ""

    sentences = split_sentences(text)
    if len(sentences) <= 3:
        # 문장이 너무 적으면 그냥 원문 반환
        return text.strip()

    freq_table = build_frequency_table(text)
    if not freq_table:
        return "\n".join(sentences[: max_sentences])

    sentence_scores = score_sentences(sentences, freq_table)

    # 포함할 문장 개수 계산
    target_count = max(1, min(max_sentences, math.ceil(len(sentences) * ratio)))

    # 점수 높은 문장 순으로 정렬
    ranked_sentences = sorted(
        sentence_scores.items(), key=lambda x: x[1], reverse=True
    )
    selected_sentences = [s for s, _ in ranked_sentences[:target_count]]

    # 원래 문서 순서를 유지하면서 선택된 문장만 출력
    ordered_summary = [s for s in sentences if s in selected_sentences]

    return "\n".join(ordered_summary)
