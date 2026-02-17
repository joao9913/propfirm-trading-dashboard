from csv_parser import load_csv_file, validate_columns
from metrics import MetricsCalculator as mc
from report import render_report

filename = "US30"
path = "data/" + filename + "/"
phase_list = ["PHASE1", "PHASE2", "PHASE3", "CHALLENGE", "FUNDED"]
df_dict = {}

# Load, validate and calculate metrics for each csv file
for phase in phase_list:
    full_path = path + phase + ".csv"

    df = load_csv_file(full_path)
    validate_columns(df)
    df_dict[phase] = df

calculator = mc(df_dict)
all_metrics = calculator.calculate_metrics()

# Load and fill html report template with calculated metrics
render_report(all_metrics, "report_html.html", filename)