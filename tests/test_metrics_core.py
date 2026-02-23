import pandas as pd
import pytest
from propfirm_trading_dashboard.metrics import MetricsCalculator

def test_p1_p2_metrics():
    df_phase1 = pd.DataFrame({
        "Challenge Number": [1, 2, 3],
        "Start Phase Date": ["2013.01.01", "2013.01.15", "2013.01.21"],
        "End Phase Date": ["2013.01.15", "2013.01.21", "2013.02.07"],
        "Phase": [1, 1, 1],
        "Outcome": ["Passed", "Passed", "Failed"],
        "Reason": ["Profit Target", "Profit Target", "Max Drawdown"],
        "Duration": [14, 6, 42],
        "Start Balance": [10000.00, 10801.42, 16523.2],
        "Ending Balance": [10801.42, 11638.97, 15512.64],
        "Max Drawdown": [9000.00, 9801.42, 15523.29],
        "Profit Target": [10800, 11601.42, 17323.29],
        "Daily Drawdown": [54.60, 27.84, 146.56]
    })

    empty_df = pd.DataFrame({
        "Challenge Number": [],
        "Start Phase Date": [],
        "End Phase Date": [],
        "Phase": [],
        "Outcome": [],
        "Reason": [],
        "Duration": [],
        "Start Balance": [],
        "Ending Balance": [],
        "Max Drawdown": [],
        "Profit Target": [],
        "Daily Drawdown": []
    })

    dfs = {
        "phase1": df_phase1,
        "phase2": df_phase1.copy(),
        "phase3": empty_df,
        "challenge": empty_df,
        "funded": empty_df
    }

    calculator = MetricsCalculator(dfs)
    results = calculator.calculate_metrics()
    p1 = results["phase1"]

    assert p1["p1_number_passed_challenges"] == 2
    assert p1["p1_number_failed_challenges"] == 1
    assert p1["p1_number_challenges"] == 3
    assert p1["p1_challenge_winrate"] == 66.67
    assert p1["p1_max_cons_challenge_passed"] == 2
    assert p1["p1_max_cons_challenge_failed"] == 1
    assert p1["p1_average_challenge_duration"] == 20.67
    assert p1["p1_average_challenge_passed_duration"] == 10
    assert p1["p1_average_challenge_failed_duration"] == 42
    assert p1["p1_average_cons_challenge_passed"] == 2
    assert p1["p1_average_cons_challenge_failed"] == 1
    assert p1["p1_efficiency_ratio"] == 3.23