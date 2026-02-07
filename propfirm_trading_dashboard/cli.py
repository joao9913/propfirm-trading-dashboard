from csv_parser import load_csv_file, validate_columns
from metrics import MetricsCalculator as mc
from report import read_html_template

path = "data/"
phase_list = ["phase1", "phase2", "phase3", "challenge", "funded"]
df_dict = {}

for phase in phase_list:
    full_path = path + phase + ".csv"

    df = load_csv_file(full_path)
    validate_columns(df)
    df_dict[phase] = df

calculator = mc(df_dict)
#all_metrics = calculator.calculate_metrics()
print(df_dict)