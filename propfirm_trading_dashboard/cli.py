from simulation_run import run_single_simulation, run_joined_simulation
from pathlib import Path

phase_list = ["phase1", "phase2", "phase3", "challenge", "funded"]

while True:
    print("Select mode:")
    print("1 - Single Simulation")
    print("2 - Joined Simulation")
    print("q - Quit")

    choice = input("Enter your choice: ").strip().lower()

    if choice == "q":
        break

    elif choice == "1":
        while True:
            folder_name = input("Enter strategy folder name: ").strip()
            folder_path = Path(folder_name)
            if folder_path.is_dir():
                break;
            else:
                print("Folder does not exist. Please enter a valid run name.")
                
        run_single_simulation(folder_name, phase_list)

    elif choice == "2":
        run_joined_simulation("data", phase_list)

    else:
        print("Invalid choice")