from pathlib import Path

def read_html_template(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def replace_placeholders(metrics: dict, html_file: str):
    html_content = html_file

    for phase, phase_metrics in metrics.items():
        for metric_key, metric_value in phase_metrics.items():
            print(metric_key, metric_value)

    return html_content