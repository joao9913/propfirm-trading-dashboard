from csv_parser import load_csv_file, validate_columns
from metrics import MetricsCalculator as mc
from report import render_report
from multi_strategy_loader import discover_strategy_groups, merge_group_phase

phase_list = ["phase1", "phase2", "phase3", "challenge", "funded"]

def run_joined_simulation(base_path: str, phase_list: list):
    groups = discover_strategy_groups(base_path)

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
    render_report(all_metrics, "report_html.html", "JoinedSimulation")

def run_single_simulation(filename: str):
    path = "data/" + filename + "/"
    df_dict = {}

    for phase in phase_list:
        full_path = path + phase + ".csv"

        df = load_csv_file(full_path)
        validate_columns(df)
        df_dict[phase] = df

    calculator = mc(df_dict)
    all_metrics = calculator.calculate_metrics()
    render_report(all_metrics, "report_html.html", filename)


while True:
    print("Select mode:")
    print("1 - Single Simulation")
    print("2 - Joined Simulation")
    print("q - Quit")

    choice = input("Enter your choice: ").strip().lower()

    if choice == "q":
        break
    elif choice == "1":
        folder_name = input("Enter strategy folder name for single simulation: ").strip()
        run_single_simulation(folder_name)
    elif choice == "2":
        run_joined_simulation("data", phase_list)
    else:
        print("Invalid choice")