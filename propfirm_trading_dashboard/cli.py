from csv_parser import load_csv_file, validate_columns
from metrics import MetricsCalculator as mc

phase_type = "phase1"
filename = phase_type + ".csv"
path = "data/" + filename

#Load and validate columns of csv file
df = load_csv_file(path)
validate_columns(df, filename)

#Calculate metrics of csv file
calculator = mc(df)

calculator.calculate_metrics(phase_type)