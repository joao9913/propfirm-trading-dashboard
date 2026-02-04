import pandas as pd

def load_csv_file(file_path: str):
    df = pd.read_csv(file_path, encoding='utf-16', sep='\t')

    return df