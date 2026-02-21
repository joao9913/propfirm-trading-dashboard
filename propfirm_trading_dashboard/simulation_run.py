import pandas as pd
from csv_parser import load_csv_file, validate_columns
from metrics import MetricsCalculator as mc
from report import render_report
from multi_strategy_loader import discover_strategy_groups, merge_group_phase


def run_joined_simulation(base_path: str, phase_list: list):
    groups = discover_strategy_groups(base_path)

    all_folders = []
    for folder_list in groups.values():
        all_folders.extend(folder_list)

    print(f"Processing joined simulation for {len(all_folders)} folders...")

    df_dict = {}
    all_runs = []

    for phase in phase_list:
        merged_df = merge_group_phase(base_path, all_folders, phase)
        df_dict[phase] = merged_df

        if not merged_df.empty:
            merged_df["Phase"] = phase
            all_runs.append(merged_df)

    runs_table_df = (
        pd.concat(all_runs, ignore_index=True)
        if all_runs else pd.DataFrame()
    )

    calculator = mc(df_dict)
    all_metrics = calculator.calculate_metrics()

    render_report(
        all_metrics,
        "report_html.html",
        "JoinedSimulation",
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

    render_report(
        all_metrics,
        "report_html.html",
        filename
    )