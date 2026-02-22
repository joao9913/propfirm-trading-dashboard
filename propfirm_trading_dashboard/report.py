from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def load_template(template_name: str) -> Environment:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    return template

def render_report(metrics: dict, template_name: str, filename: str, runs_table=None, monthly_pnl_table=None):
    flat_metrics = {}
    for phase_name, phase_metrics in metrics.items():
        flat_metrics.update(phase_metrics)
    
    runs_table_html = {}
    if runs_table:
        for phase, df in runs_table.items():
            if df is not None and not df.empty:
                runs_table_html[phase] = df.to_html(index=False, classes="runs_table", border=0)
    
    monthly_pnl_html = None
    if monthly_pnl_table is not None and not monthly_pnl_table.empty:
        monthly_pnl_html = monthly_pnl_table.to_html(index=False, classes="runs_table", border=0)

    template = load_template(template_name)
    output_path = "reports/" + filename + ".html"
    html_content = template.render(
        **flat_metrics,
        runs_tables_html=runs_table_html,
        monthly_pnl_table_html = monthly_pnl_html,
        FOLDER_NAME=filename
    )
    Path(output_path).write_text(html_content, encoding="utf-8")
    print(f"Report saved to {output_path}")