import pandas as pd

def load_csv_file(path: str):
    df = pd.read_csv(path, encoding='utf-16', sep='\t')
    return df

def validate_columns(df: pd.DataFrame):
    required_columns = ["Challenge Number", "Start Phase Date", "End Phase Date", "Phase", "Outcome", "Reason", "Duration", "Start Balance", "Ending Balance", "Max Drawdown", "Profit Target", "Daily Drawdown"]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"File is missing required columns: {missing_columns}")