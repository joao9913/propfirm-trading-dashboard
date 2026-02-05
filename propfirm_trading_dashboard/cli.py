from csv_parser import load_csv_file, validate_columns

filename = "test_fail.csv"
path = "data/" + filename

df = load_csv_file(path)
print(validate_columns(df, filename))