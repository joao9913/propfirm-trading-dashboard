import pandas as pd
from csv_parser import load_csv_file, validate_columns
from metrics import MetricsCalculator as mc
from report import render_report
from multi_strategy_loader import discover_strategy_groups, merge_group_phase
from datetime import datetime

def run_joined_simulation(base_path: str, phase_list: list):
    groups = discover_strategy_groups(base_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"JoinedSimulation_{timestamp}"

    all_folders = []
    for folder_list in groups.values():
        all_folders.extend(folder_list)

    print(f"Processing joined simulation for {len(all_folders)} folders...")

    df_dict = {}

    for phase in phase_list:
        merged_df = merge_group_phase(base_path, all_folders, phase)
        df_dict[phase] = merged_df

    runs_table_df = build_runs_table(df_dict)

    calculator = mc(df_dict)
    all_metrics = calculator.calculate_metrics()

    render_report(
        all_metrics,
        "report_html.html",
        report_name,
        runs_table=runs_table_df
    )


def run_single_simulation(filename: str, phase_list: list):
    path = "data/" + filename + "/"
    df_dict = {}

    for phase in phase_list:
        full_path = path + phase + ".csv"

        df = load_csv_file(full_path)
        validate_columns(df)
        df_dict[phase] = df

    calculator = mc(df_dict)
    all_metrics = calculator.calculate_metrics()

    runs_table_df = build_runs_table(df_dict)

    render_report(
        all_metrics,
        "report_html.html",
        filename,
        runs_table=runs_table_df
    )

def build_runs_table(df_dict: dict) -> pd.DataFrame:
    all_runs = []

    for phase, df in df_dict.items():
        if df is not None and not df.empty:
            df_copy = df.copy()
            df_copy["Phase"] = phase
            all_runs.append(df_copy)

    if not all_runs:
        return pd.DataFrame()
    
    merged = pd.concat(all_runs, ignore_index=True)
    merged = merged.rename(columns={
        "Start Phase Date": "Start Date",
        "End Phase Date": "End Date",
    })
    columns_to_keep=[
        "Challenge Number",
        "Start Date",
        "End Date",
        "Phase",
        "Outcome",
        "Duration",
        "PnL",
        "Month",
    ]

    existing_columns = [col for col in columns_to_keep if col in merged.columns]
    return merged[existing_columns]