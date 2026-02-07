from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def load_template(template_name: str) -> Environment:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    return template

def render_report(metrics: dict, template_name: str, output_path: str):
    flat_metrics = {}
    for phase, metrics in metrics.items():
        flat_metrics.update(metrics)

    template = load_template(template_name)
    html_content = template.render(**flat_metrics)
    Path(output_path).write_text(html_content, encoding = "utf-8")
    print(f"Report saved to {output_path}")