from csv_parser import load_csv_file, validate_columns
from metrics import MetricsCalculator as mc
from report import read_html_template

phase_type = "funded"
filename = phase_type + ".csv"
path = "data/" + filename

#Load and validate columns of csv file
df = load_csv_file(path)
validate_columns(df, filename)

#Calculate metrics of csv file
calculator = mc(df)

# Generate html report 
# read_html_template("templates/report_html.html")