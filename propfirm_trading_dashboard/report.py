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
        def format_pnl(val):
            if isinstance(val, (int, float)):
                formatted = f"{val:,.2f}"

                if val < 0:
                    return f'<span class="neg">{formatted}</span>'
                elif val > 0:
                    return f'<span class="pos">{formatted}</span>'
                else:
                    return formatted

            return val

        styled_table = monthly_pnl_table.copy()

        for col in styled_table.columns:
            if col != "Year":
                styled_table[col] = styled_table[col].apply(format_pnl)

        monthly_pnl_html = styled_table.to_html(
            index=False,
            classes="runs_table",
            border=0,
            escape=False
        )

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