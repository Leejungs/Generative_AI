from pathlib import Path


def ensure_output_dir(path: str) -> Path:
    """
    출력 디렉터리가 없으면 생성하고, Path 객체를 반환합니다.
    """
    out_dir = Path(path)
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir
