import pandas as pd

class MetricsCalculator:
    def __init__(self, df):
        self.df = df
    
    def calculate_metrics(self, phase_type: str):
        dispatch_types = {
        "phase1": self._calculate_metrics_phase1_2,
        "phase2": self._calculate_metrics_phase1_2,
        "phase3": self._calculate_metrics_phase3,
        "challenge": self._calculate_metrics_challenge,
        "funded": self._calculate_metrics_funded,
        }

        if phase_type not in dispatch_types:
            raise ValueError("Invalid phase_type")
        
        return dispatch_types[phase_type]()


    #Private methods for calculating metrics depending on phase
    def _calculate_metrics_phase1_2(self):
        self.df["Duration"] = self.df["Duration"].astype(float)
        outcome_series = self.df["Outcome"]

        number_passed = (outcome_series == "Passed").sum()
        number_failed = (outcome_series == "Failed").sum()
        total_outcomes = number_failed + number_passed
        winrate = round((number_passed / total_outcomes) * 100, 2) if total_outcomes else 0
        average_duration = round(self.df["Duration"].mean(), 2) if total_outcomes else 0
        average_duration_passed = round(self.df[outcome_series == "Passed"]["Duration"].mean(), 2)
        average_duration_failed = round(self.df[outcome_series == "Failed"]["Duration"].mean(), 2)

        efficiency_ratio = round(winrate / average_duration, 2)

    def _calculate_metrics_phase3(self):
        print("Calculating Phase 3")

    def _calculate_metrics_challenge(self):
        print("Calculating Challenge")

    def _calculate_metrics_funded(self):
        print("Calculating Funded")

    def _calculate_consecutive_metrics(self):
        print("calculate consecutive metrics")