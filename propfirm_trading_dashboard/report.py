from pathlib import Path

def read_html_template(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def replace_placeholders():
    pass