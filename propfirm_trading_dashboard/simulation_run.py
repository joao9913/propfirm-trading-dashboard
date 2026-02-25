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

    calculator = mc(df_dict)
    all_metrics = calculator.calculate_metrics()
    runs_table_df = build_runs_table(df_dict)

    render_report(
        all_metrics,
        "report_html.html",
        report_name,
        runs_table=runs_table_df,
        monthly_pnl_table = build_monthly_pnl(runs_table_df["funded"])
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
        runs_table=runs_table_df,
        monthly_pnl_table = build_monthly_pnl(runs_table_df["funded"])
    )

def build_runs_table(df_dict: dict) -> dict:
    tables_per_phase = {}

    columns_to_keep = [
        "Strategy_Pair",
        "Challenge Number",
        "Start Phase Date",
        "End Phase Date",
        "Phase",
        "Outcome",
        "Duration",
        "PnL",
    ]

    for phase, df in df_dict.items():
        if df is not None and not df.empty:
            df_copy = df.copy()
            existing_columns = [col for col in columns_to_keep if col in df_copy]
            df_copy = df_copy[existing_columns]
            df_copy = df_copy.rename(columns={
                "Start Phase Date": "Start Date",
                "End Phase Date": "End Date",
                "Challenge Number": "Run #"
            })
            tables_per_phase[phase] = df_copy
    return tables_per_phase

def build_monthly_pnl(runs_table: pd.DataFrame) -> pd.DataFrame:
    if isinstance(runs_table, dict):
        df_all = pd.concat([df for df in runs_table.values() if df is not None and not df.empty])
    else:
        df_all = runs_table.copy()
    
    if 'PnL' not in df_all.columns:
        df_all['PnL'] = df_all["Ending Balance"] - df_all["Start Balance"]

    df_all.loc[df_all["PnL"] > 0, "PnL"] *= 0.67
    
    df_all["End Date"] = pd.to_datetime(df_all["End Date"], format="%Y.%m.%d")
    df_all["Year"] = df_all["End Date"].dt.year
    df_all["Month"] = df_all["End Date"].dt.month

    monthly = df_all.groupby(["Year", "Month"])["PnL"].sum().reset_index()

    table = monthly.pivot_table(index="Year", columns="Month", values = "PnL",fill_value=0).fillna(0)
    table.columns.name = None

    month_names = {i: name for i, name in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}
    table = table.rename(columns=month_names)

    table["Yearly Total"] = table.sum(axis=1)

    table = table.reset_index().sort_values("Year", ascending=False)
    return table

def build_funded_outcomes(runs_table: pd.DataFrame) -> pd.DataFrame:
    if isinstance(runs_table, dict):
        df_all = pd.concat([df for df in runs_table.values() if df is not None and not df.empty])
    else:
        df_all = runs_table.copy()
    
    if 'PnL' not in df_all.columns:
        df_all['PnL'] = df_all["Ending Balance"] - df_all["Start Balance"]
    df_all.loc[df_all["PnL"] > 0, "PnL"] *= 0.67

    