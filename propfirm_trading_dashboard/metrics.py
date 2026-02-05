import pandas as pd

class MetricsCalculator:
    def __init__(self, df):
        self.df = df
    
    def calculate_metrics(self, phase_type: str):
        dispatch_types = {
        "phase1": self._calculate_metrics_phase1,
        "phase2": self._calculate_metrics_phase2,
        "phase3": self._calculate_metrics_phase3,
        "challenge": self._calculate_metrics_challenge,
        "funded": self._calculate_metrics_funded,
        }

        if phase_type not in dispatch_types:
            raise ValueError("Invalid phase_type")
        
        return dispatch_types[phase_type]()


    #Private methods for calculating metrics depending on phase
    def _calculate_metrics_phase1(self):
        print("Calculating Phase 1")

    def _calculate_metrics_phase2(self):
        print("Calculating Phase 2")

    def _calculate_metrics_phase3(self):
        print("Calculating Phase 3")

    def _calculate_metrics_challenge(self):
        print("Calculating Challenge")

    def _calculate_metrics_funded(self):
        print("Calculating Funded")