from csv_parser import load_csv_file

df = load_csv_file("data/test_file.csv")

print(df.head())