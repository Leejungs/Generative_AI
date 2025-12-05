# 📝 PDF 요약 및 자동 목차 생성기  
> **PDF 문서를 입력하면 핵심 요약 + 자동 목차를 생성하는 AI 기반 도구**

---

## 📌 프로젝트 개요

이 프로젝트는 **긴 PDF 문서의 핵심 내용을 자동으로 요약**하고, **문단 구조를 분석하여 자동 목차(Table of Contents, TOC)** 를 생성하는 AI 도구입니다.  
보고서·논문·과제 등 텍스트가 많은 문서를 빠르게 파악하도록 도와 시간을 절약하고 문서 활용 효율을 높이는 것을 목표로 합니다.

---

## 🚀 주요 기능

- **PDF → 텍스트 자동 추출**
- **요약 모델을 활용한 핵심 요약 자동 생성**
- **문단 패턴 기반 자동 목차 생성**
- **CLI 실행 지원 (main.py 한 줄 실행)**
- **한국어·영어 문서 모두 지원**

---

## 🛠 기술 스택

- **Python 3.11**
- 라이브러리  
  - `PyPDF2` 또는 `pdfplumber` — PDF 텍스트 추출  
  - `transformers` — 요약 모델 (Pegasus / BART 기반)  
  - `regex`, `nltk` — 문단 분석 및 전처리  
  - `argparse` — CLI 옵션 처리  

---

## 📦 설치 방법

### 1) 가상환경 생성 (선택)
```bash
python -m venv .venv
source .venv/bin/activate       # Windows → .venv\Scripts\activate
```
### 2) 패키지 설치
```bash
pip install -r requirements.txt
```

### 3)📁 프로젝트 구조 (예시)
```bash
📦 pdf-summary-toc
 ┣ 📂 outputs
 ┃ ┣ summary.txt
 ┃ ┗ toc.txt
 ┣ 📂 src
 ┃ ┣ extractor.py
 ┃ ┣ summarizer.py
 ┃ ┣ toc_generator.py
 ┃ ┗ utils.py
 ┣ main.py
 ┣ requirements.txt
 ┗ README.md
```
