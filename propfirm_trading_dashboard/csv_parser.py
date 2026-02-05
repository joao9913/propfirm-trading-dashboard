import pandas as pd

# Dictionaries to define which columns each simulation run should have
simulation_types = {
    "phase1.csv": ["Challenge Number", "Start Phase Date", "End Phase Date", "Phase", "Outcome", "Reason", "Duration", "Start Balance", "Ending Balance", "Max Drawdown", "Profit Target", "Daily Drawdown"],
    "phase2.csv": [""],
    "phase3.csv": [""],
    "challenge.csv": [""],
    "funded.csv": [""],
}

def load_csv_file(path: str):
    df = pd.read_csv(path, encoding='utf-16', sep='\t')
    return df

def validate_columns(df: pd.DataFrame, filename: str):


    return None