from csv_parser import load_csv_file, validate_columns

filename = "phase1.csv"
path = "data/" + filename

df = load_csv_file(path)
validate_columns(df, filename)

print(df.head())