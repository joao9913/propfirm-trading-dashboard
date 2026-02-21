import os
from typing import Dict, List

def discover_strategy_groups(base_path: str) -> Dict[str, List[str]]:
    groups = {}

    for folder in os.listdir(base_path):
        full_path = os.path.join(base_path, folder)

        if not os.path.isdir(full_path):
            continue

        try:
            strategy_pair, run_id = folder.rsplit("_", 1)
            strategy_name, pair = strategy_pair.rsplit("_", 1)
        except ValueError:
            continue

        group_key = strategy_name
        groups.setdefault(group_key, []).append(folder)

    return groups

import pandas as pd
from csv_parser import load_csv_file, validate_columns

def merge_group_phase(base_path: str, folders: List[str], phase_name: str) -> pd.DataFrame:
    dfs = []

    for folder in folders:
        file_path = os.path.join(base_path, folder, f"{phase_name}.csv")

        if not os.path.exists(file_path):
            continue

        df = load_csv_file(file_path)
        validate_columns(df)

        df["Strategy_Pair"] = "_".join(folder.split("_")[:2])
        df["Run"] = folder.rsplit("_", 1)[-1]

        dfs.append(df)

    if not dfs:
        return pd.DataFrame(columns=[
            "Challenge Number", "Start Phase Date", "End Phase Date", 
            "Phase", "Outcome", "Reason", "Duration", 
            "Start Balance", "Ending Balance", "Max Drawdown", 
            "Profit Target", "Daily Drawdown", "PnL"
        ])
    
    merged = pd.concat(dfs, ignore_index=True)

    merged["End Phase Date"] = pd.to_datetime(merged["End Phase Date"], format="%Y.%m.%d")
    merged.sort_values("End Phase Date", inplace = True)
    cols = merged.columns.tolist()
    if "Strategy_Pair" in cols:
        cols.insert(0, cols.pop(cols.index("Strategy_Pair")))
    merged = merged[cols]
    return merged