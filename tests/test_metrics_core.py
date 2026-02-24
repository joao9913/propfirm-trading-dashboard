import pandas as pd
import pytest
from propfirm_trading_dashboard.metrics import MetricsCalculator

def test_empty_data():
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
        "phase1": empty_df,
        "phase2": empty_df,
        "phase3": empty_df,
        "challenge": empty_df,
        "funded": empty_df
    }

    calculator = MetricsCalculator(dfs)
    results = calculator.calculate_metrics()
    p1 = results["phase1"]
    p2 = results["phase2"]
    p3 = results["phase3"]
    c = results["challenge"]
    f = results["funded"]

    for key, value in p1.items():
        assert value == 0
    
    for key, value in p2.items():
        assert value == 0
    
    for key, value in p3.items():
        assert value == 0
    
    for key, value in c.items():
        assert value == 0
    
    for key, value in f.items():
        assert value == 0  

def test_single_p1_p2_metrics():
    df_phase1_single = pd.DataFrame({
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
        "phase1": df_phase1_single,
        "phase2": df_phase1_single.copy(),
        "phase3": empty_df,
        "challenge": empty_df,
        "funded": empty_df
    }

    calculator = MetricsCalculator(dfs)
    results = calculator.calculate_metrics()
    p1 = results["phase1"]
    p2 = results["phase2"]

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

    assert p2["p2_number_passed_challenges"] == 2
    assert p2["p2_number_failed_challenges"] == 1
    assert p2["p2_number_challenges"] == 3
    assert p2["p2_challenge_winrate"] == 66.67
    assert p2["p2_max_cons_challenge_passed"] == 2
    assert p2["p2_max_cons_challenge_failed"] == 1
    assert p2["p2_average_challenge_duration"] == 20.67
    assert p2["p2_average_challenge_passed_duration"] == 10
    assert p2["p2_average_challenge_failed_duration"] == 42
    assert p2["p2_average_cons_challenge_passed"] == 2
    assert p2["p2_average_cons_challenge_failed"] == 1
    assert p2["p2_efficiency_ratio"] == 3.23

def test_single_p3_metrics():
    df_phase3_single = pd.DataFrame({
        "Challenge Number": [1, 2, 3],
        "Start Phase Date": ["2013.01.01", "2013.01.15", "2013.01.21"],
        "End Phase Date": ["2013.01.15", "2013.01.21", "2013.02.07"],
        "Phase": [3, 3, 3],
        "Outcome": ["Payout", "Payout", "Failed"],
        "Reason": ["Payout", "Payout", "Max Drawdown"],
        "Duration": [14, 6, 42],
        "Start Balance": [10000.00, 10402.58, 13713.90],
        "Ending Balance": [10402.58, 10809.36, 12705.88],
        "Max Drawdown": [9000.00, 9402.58, 12713.90],
        "Profit Target": [10400, 10802.58, 14113.90],
        "Daily Drawdown": [0.00, 0.00, 203.68]
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
        "phase1": empty_df,
        "phase2": empty_df,
        "phase3": df_phase3_single,
        "challenge": empty_df,
        "funded": empty_df
    }

    calculator = MetricsCalculator(dfs)
    results = calculator.calculate_metrics()
    p3 = results["phase3"]

    assert p3["p3_number_payouts"] == 2
    assert p3["p3_number_failed_challenges"] == 1
    assert p3["p3_number_challenges"] == 3
    assert p3["p3_payout_winrate"] == 66.67
    assert p3["p3_average_challenge_duration"] == 20.67
    assert p3["p3_average_challenge_passed_duration"] == 10
    assert p3["p3_average_challenge_failed_duration"] == 42
    assert p3["p3_max_cons_payouts"] == 2
    assert p3["p3_max_cons_failed"] == 1
    assert p3["p3_average_max_cons_payouts"] == 2
    assert p3["p3_average_max_cons_failed"] == 1
    assert p3["p3_average_profit_payout"] == 404.68
    assert p3["p3_total_profit_payouts"] == 809.36
    assert p3["p3_total_loss_payouts"] == 80
    assert p3["p3_profit_factor"] == 10.12
    assert p3["p3_profitability_ratio"] == 33.73

def test_single_challenge_metrics():
    df_challenge_single = pd.DataFrame({
    "Challenge Number": [4, 4, 5, 5, 10],
    "Start Phase Date": ["2013.03.11", "2013.04.15", "2013.04.22", "2013.05.14", "2014.02.24"],
    "End Phase Date": ["2013.04.15", "2013.04.22", "2013.05.14", "2013.06.26", "2014.03.07"],
    "Phase": [1, 2, 1, 2, 1],
    "Outcome": ["Passed", "Passed", "Passed", "Failed", "Failed"],
    "Reason": ["Profit Target", "Profit Target", "Profit Target", "Max Drawdown", "Max Drawdown"],
    "Duration": [35, 7, 21, 43, 11],
    "Start Balance": [13932.62, 14746.41, 15254.41, 16089.73, 17595.13],
    "Ending Balance": [14746.41, 15254.41, 16089.73, 15068.55, 16595.07],
    "Max Drawdown": [12932.62, 13746.41, 14254.41, 15089.73, 16595.13],
    "Profit Target": [14732.62, 15246.41, 16054.41, 16589.73, 18395.13],
    "Daily Drawdown": [310.59, 159.34, 212.52, 94.50, 302.40]
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
        "phase1": empty_df,
        "phase2": empty_df,
        "phase3": empty_df,
        "challenge": df_challenge_single,
        "funded": empty_df
    }

    calculator = MetricsCalculator(dfs)
    results = calculator.calculate_metrics()
    c = results["challenge"]

    assert c["c_number_challenges"] == 3
    assert c["c_number_passed_challenges"] == 1
    assert c["c_number_failed_challenges"] == 2
    assert c["c_challenge_winrate"] == 33.33
    assert c["c_average_challenge_duration"] == 39
    assert c["c_average_challenge_passed_duration"] == 42
    assert c["c_average_challenge_failed_duration"] == 37.5
    assert c["c_max_cons_challenge_passed"] == 1
    assert c["c_max_cons_challenge_failed"] == 2
    assert c["c_average_cons_challenge_passed"] == 1
    assert c["c_average_cons_challenge_failed"] == 2
    assert c["c_failed_p1_percentage"] == 50
    assert c["c_failed_p2_percentage"] == 50
    assert c["c_efficiency_ratio"] == 0.85

def test_single_funded_metrics():
    df_funded_single = pd.DataFrame({
    "Challenge Number": [1, 1, 1, 1, 1, 2, 3, 3, 3],
    "Start Phase Date": ["2013.01.01", "2013.01.15", "2013.01.21", "2013.02.04", "2014.02.20", "2014.03.13", "2014.04.04", "2014.04.17", "2014.06.09"],
    "End Phase Date": ["2013.01.15", "2013.01.21", "2013.02.04", "2013.02.19", "2014.03.13","2014.04.04", "2014.04.17", "2014.06.09", "2014.08.01"],
    "Phase": [1, 2, 3, 3, 3, 1, 1, 2, 3],
    "Outcome": ["Passed", "Passed", "Payout", "Payout", "Failed", "Failed", "Passed", "Passed", "Payout"],
    "Reason": ["Profit Target", "Profit Target", "Payout", "Payout", "Max Drawdown", "Max Drawdown", "Profit Target", "Profit Target", "Payout"],
    "Duration": [14, 6, 14, 15, 20, 22, 12, 53, 52],
    "Start Balance": [10000.00, 10801.42, 11306.69, 11706.85, 14249.71, 13241.69, 12239.40, 13050.23, 13569.93],
    "Ending Balance": [10801.42, 11306.69, 11706.85, 11893.17, 13241.69,12239.40, 13050.23, 13569.93, 13755.28],
    "Max Drawdown": [9000.00, 9801.42, 10306.69, 10706.85, 13249.71, 12241.69, 11239.40, 12050.23, 12569.93],
    "Profit Target": [10800.00, 11301.42, 11706.69, 12106.85, 14649.71, 14041.69, 13039.40, 13550.23, 13969.93],
    "Daily Drawdown": [54.60, 22.40, 0.00, 73.78, 203.68, 118.61, 5.52, 95.94, 26.04]
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
        "phase1": empty_df,
        "phase2": empty_df,
        "phase3": empty_df,
        "challenge": empty_df,
        "funded": df_funded_single
    }

    calculator = MetricsCalculator(dfs)
    results = calculator.calculate_metrics()
    f = results["funded"]

    assert f["f_number_challenges"] == 3
    assert f["f_number_passed_challenges"] == 2
    assert f["f_number_failed_challenges"] == 1
    assert f["f_challenge_winrate"] == 66.67
    assert f["f_average_challenge_duration"] == 57.67
    assert f["f_average_challenge_passed_duration"] == 75.5
    assert f["f_average_challenge_failed_duration"] == 22
    assert f["f_max_cons_challenge_passed"] == 1
    assert f["f_max_cons_challenge_failed"] == 1
    assert f["f_average_cons_challenge_passed"] == 1
    assert f["f_average_cons_challenge_failed"] == 1
    assert f["f_average_profit_challenge"] == 230.61
    assert f["f_challenge_efficiency_ratio"] == 230.61
    assert f["f_payout_winrate"] == 75
    assert f["f_max_cons_payouts"] == 2
    assert f["f_average_payouts_challenge"] == 1.5
    assert f["f_average_profit_payout"] == 257.28
    assert f["f_profitability_ratio"] == 3.62

def test_joined_p1_p2_metrics():

    data = [
        ["HourBreakout_USDJPY", 1, "2013-01-01", "2013-01-09", 1, "Passed", "Profit Target", 8, 10000.0, 10821.55, 9000.0, 10800.0, 214.7],
        ["HourBreakout_GBPUSD", 1, "2013-01-01", "2013-01-15", 1, "Passed", "Profit Target", 14, 10000.0, 10801.42, 9000.0, 10800.0, 54.6],
        ["HourBreakout_USDJPY", 2, "2013-01-09", "2013-01-17", 1, "Failed", "Max Drawdown", 8, 10821.55, 9819.18, 9821.55, 11621.55, 371.51],
        ["HourBreakout_GBPUSD", 2, "2013-01-15", "2013-01-21", 1, "Passed", "Profit Target", 6, 10801.42, 11638.97, 9801.42, 11601.42, 27.84],
        ["HourBreakout_USDJPY", 3, "2013-01-17", "2013-02-06", 1, "Failed", "Max Drawdown", 19, 9819.18, 8806.58, 8819.18, 10619.18, 263.13],
        ["HourBreakout_GBPUSD", 3, "2013-01-21", "2013-02-07", 1, "Passed", "Profit Target", 16, 11638.97, 12454.37, 10638.97, 12438.97, 114.26],
        ["HourBreakout_GBPUSD", 4, "2013-02-07", "2013-02-12", 1, "Passed", "Profit Target", 5, 12454.37, 13255.7, 11454.37, 13254.37, 60.26],
    ]

    columns = [
        "Strategy_Pair",
        "Challenge Number",
        "Start Phase Date",
        "End Phase Date",
        "Phase",
        "Outcome",
        "Reason",
        "Duration",
        "Start Balance",
        "Ending Balance",
        "Max Drawdown",
        "Profit Target",
        "Daily Drawdown"
    ]

    df_phase1_joined = pd.DataFrame(data, columns = columns)

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
        "phase1": df_phase1_joined,
        "phase2": df_phase1_joined.copy(),
        "phase3": empty_df,
        "challenge": empty_df,
        "funded": empty_df
    }

    calculator = MetricsCalculator(dfs)
    results = calculator.calculate_metrics()
    p1 = results["phase1"]
    p2 = results["phase2"]

    assert p1["p1_number_passed_challenges"] == 5
    assert p1["p1_number_failed_challenges"] == 2
    assert p1["p1_number_challenges"] == 7
    assert p1["p1_challenge_winrate"] == 71.43
    assert p1["p1_max_cons_challenge_passed"] == 2
    assert p1["p1_max_cons_challenge_failed"] == 1
    assert p1["p1_average_challenge_duration"] == 10.86
    assert p1["p1_average_challenge_passed_duration"] == 9.8
    assert p1["p1_average_challenge_failed_duration"] == 13.5
    assert p1["p1_average_cons_challenge_passed"] == 1.67
    assert p1["p1_average_cons_challenge_failed"] == 1
    assert p1["p1_efficiency_ratio"] == 6.58

    assert p2["p2_number_passed_challenges"] == 5
    assert p2["p2_number_failed_challenges"] == 2
    assert p2["p2_number_challenges"] == 7
    assert p2["p2_challenge_winrate"] == 71.43
    assert p2["p2_max_cons_challenge_passed"] == 2
    assert p2["p2_max_cons_challenge_failed"] == 1
    assert p2["p2_average_challenge_duration"] == 10.86
    assert p2["p2_average_challenge_passed_duration"] == 9.8
    assert p2["p2_average_challenge_failed_duration"] == 13.5
    assert p2["p2_average_cons_challenge_passed"] == 1.67
    assert p2["p2_average_cons_challenge_failed"] == 1
    assert p2["p2_efficiency_ratio"] == 6.58

def test_joined_p3_metrics():

    data = [
        ["HourBreakout_GBPUSD", 1, "2013-01-01", "2013-01-15", 3, "Payout", "Payout", 14, 10000.0, 10402.58, 9000.0, 10400.0, 0.0],
        ["HourBreakout_USDJPY", 1, "2013-01-01", "2013-01-15", 3, "Payout", "Payout", 14, 10000.0, 10405.29, 9000.0, 10400.0, 0.0],
        ["HourBreakout_GBPUSD", 2, "2013-01-15", "2013-01-29", 3, "Payout", "Payout", 14, 10402.58, 10809.36, 9402.58, 10802.58, 0.0],
        ["HourBreakout_USDJPY", 2, "2013-01-15", "2013-02-07", 3, "Failed", "Max Drawdown", 23, 10405.29, 9394.72, 9405.29, 10805.29, 343.14],
        ["HourBreakout_GBPUSD", 3, "2013-01-29", "2013-02-12", 3, "Payout", "Payout", 14, 10809.36, 11218.74, 9809.36, 11209.36, 0.0],
        ["HourBreakout_USDJPY", 3, "2013-02-07", "2013-02-21", 3, "Payout", "Payout", 14, 9394.72, 9806.38, 8394.72, 9794.72, 0.0],
        ["HourBreakout_GBPUSD", 4, "2013-02-12", "2013-02-26", 3, "Payout", "Payout", 14, 11218.74, 11398.91, 10218.74, 11618.74, 13.64],
    ]

    columns = [
        "Strategy_Pair",
        "Challenge Number",
        "Start Phase Date",
        "End Phase Date",
        "Phase",
        "Outcome",
        "Reason",
        "Duration",
        "Start Balance",
        "Ending Balance",
        "Max Drawdown",
        "Profit Target",
        "Daily Drawdown"
    ]

    df_phase3_joined = pd.DataFrame(data, columns=columns)

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
        "phase1": empty_df,
        "phase2": empty_df,
        "phase3": df_phase3_joined,
        "challenge": empty_df,
        "funded": empty_df
    }

    calculator = MetricsCalculator(dfs)
    results = calculator.calculate_metrics()
    p3 = results["phase3"]

    assert p3["p3_number_payouts"] == 6
    assert p3["p3_number_failed_challenges"] == 1
    assert p3["p3_number_challenges"] == 7
    assert p3["p3_payout_winrate"] == 85.71
    assert p3["p3_average_challenge_duration"] == 15.29
    assert p3["p3_average_challenge_passed_duration"] == 14.0
    assert p3["p3_average_challenge_failed_duration"] == 23
    assert p3["p3_max_cons_payouts"] == 3
    assert p3["p3_max_cons_failed"] == 1
    assert p3["p3_average_max_cons_payouts"] == 3
    assert p3["p3_average_max_cons_failed"] == 1
    assert p3["p3_average_profit_payout"] == 369.31
    assert p3["p3_total_profit_payouts"] == 2215.86
    assert p3["p3_total_loss_payouts"] == 80
    assert p3["p3_profit_factor"] == 27.7
    assert p3["p3_profitability_ratio"] == 39.57

def test_joined_challenge_metrics():
    data = [
        ["HourBreakout_USDJPY", 1, "2013-01-01", "2013-01-09", 1, "Passed", "Profit Target", 8, 10000.0, 10821.55, 9000.0, 10800.0, 214.7],
        ["HourBreakout_GBPUSD", 1, "2013-01-01", "2013-01-15", 1, "Passed", "Profit Target", 14, 10000.0, 10801.42, 9000.0, 10800.0, 54.6],
        ["HourBreakout_GBPUSD", 1, "2013-01-15", "2013-01-21", 2, "Passed", "Profit Target", 6, 10801.42, 11306.69, 9801.42, 11301.42, 22.4],
        ["HourBreakout_USDJPY", 1, "2013-01-09", "2013-01-21", 2, "Failed", "Max Drawdown", 11, 10821.55, 9816.68, 9821.55, 11321.55, 6.94],
        ["HourBreakout_GBPUSD", 2, "2013-01-21", "2013-02-07", 1, "Passed", "Profit Target", 16, 11306.69, 12122.09, 10306.69, 12106.69, 114.26],
        ["HourBreakout_GBPUSD", 2, "2013-02-07", "2013-02-11", 2, "Passed", "Profit Target", 4, 12122.09, 12624.81, 11122.09, 12622.09, 3.24],
        ["HourBreakout_USDJPY", 2, "2013-01-21", "2013-02-25", 1, "Failed", "Max Drawdown", 34, 9816.68, 8577.29, 8816.68, 10616.68, 0.0],
        ["HourBreakout_USDJPY", 3, "2013-02-25", "2013-02-26", 1, "Passed", "Profit Target", 1, 8577.29, 9382.62, 7577.29, 9377.29, 38.82],
        ["HourBreakout_GBPUSD", 3, "2013-02-11", "2013-03-05", 1, "Passed", "Profit Target", 21, 12624.81, 13426.74, 11624.81, 13424.81, 11.61],
        ["HourBreakout_USDJPY", 3, "2013-02-26", "2013-03-06", 2, "Failed", "Max Drawdown", 7, 9382.62, 8379.14, 8382.62, 9882.62, 16.66],
        ["HourBreakout_USDJPY", 4, "2013-03-06", "2013-03-08", 1, "Passed", "Profit Target", 2, 8379.14, 9382.56, 7379.14, 9179.14, 114.91],
        ["HourBreakout_GBPUSD", 3, "2013-03-05", "2013-03-11", 2, "Passed", "Profit Target", 6, 13426.74, 13932.62, 12426.74, 13926.74, 14.7],
        ["HourBreakout_USDJPY", 4, "2013-03-08", "2013-03-15", 2, "Passed", "Profit Target", 6, 9382.56, 9907.99, 8382.56, 9882.56, 15.95],
    ]

    columns = [
        "Strategy_Pair",
        "Challenge Number",
        "Start Phase Date",
        "End Phase Date",
        "Phase",
        "Outcome",
        "Reason",
        "Duration",
        "Start Balance",
        "Ending Balance",
        "Max Drawdown",
        "Profit Target",
        "Daily Drawdown"
    ]

    df_challenge_joined = pd.DataFrame(data, columns=columns)

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
        "phase1": empty_df,
        "phase2": empty_df,
        "phase3": empty_df,
        "challenge": df_challenge_joined,
        "funded": empty_df
    }

    calculator = MetricsCalculator(dfs)
    results = calculator.calculate_metrics()
    c = results["challenge"]

    assert c["c_number_challenges"] == 7
    #assert c["c_number_passed_challenges"] == 4
    #assert c["c_number_failed_challenges"] == 3
    #assert c["c_challenge_winrate"] == 57.14
    #assert c["c_average_challenge_duration"] == 19.43
    #assert c["c_average_challenge_passed_duration"] == 18.75
    #assert c["c_average_challenge_failed_duration"] == 20.33
    #assert c["c_max_cons_challenge_passed"] == 2
    #assert c["c_max_cons_challenge_failed"] == 2
    #assert c["c_average_cons_challenge_passed"] == 1.33
    #assert c["c_average_cons_challenge_failed"] == 1.5
    #assert c["c_failed_p1_percentage"] == 33.33
    #assert c["c_failed_p2_percentage"] == 66.67
    #assert c["c_efficiency_ratio"] == 2.94

def test_joined_funded_metrics():
    data = [
        ["HourBreakout_USDJPY", 1, "2013-01-01", "2013-01-09", 1, "Passed", "Profit Target", 8, 10000.0, 10821.55, 9000.0, 10800.0, 214.7],
        ["HourBreakout_GBPUSD", 1, "2013-01-01", "2013-01-15", 1, "Passed", "Profit Target", 14, 10000.0, 10801.42, 9000.0, 10800.0, 54.6],
        ["HourBreakout_USDJPY", 1, "2013-01-09", "2013-01-21", 2, "Failed", "Max Drawdown", 11, 10821.55, 9816.68, 9821.55, 11321.55, 6.94],
        ["HourBreakout_GBPUSD", 1, "2013-01-15", "2013-01-21", 2, "Passed", "Profit Target", 6, 10801.42, 11306.69, 9801.42, 11301.42, 22.4],
        ["HourBreakout_GBPUSD", 1, "2013-01-21", "2013-02-04", 3, "Payout", "Payout", 14, 11306.69, 11706.85, 10306.69, 11706.69, 0.0],
        ["HourBreakout_GBPUSD", 1, "2013-02-04", "2013-02-19", 3, "Payout", "Payout", 15, 11706.85, 11893.17, 10706.85, 12106.85, 73.78],
        ["HourBreakout_USDJPY", 2, "2013-01-21", "2013-02-25", 1, "Failed", "Max Drawdown", 34, 9816.68, 8577.29, 8816.68, 10616.68, 0.0],
        ["HourBreakout_USDJPY", 3, "2013-02-25", "2013-02-26", 1, "Passed", "Profit Target", 1, 8577.29, 9382.62, 7577.29, 9377.29, 38.82],
        ["HourBreakout_GBPUSD", 1, "2013-02-19", "2013-03-05", 3, "Payout", "Payout", 14, 11893.17, 12293.68, 10893.17, 12293.17, 0.0],
        ["HourBreakout_USDJPY", 3, "2013-02-26", "2013-03-06", 2, "Failed", "Max Drawdown", 7, 9382.62, 8379.14, 8382.62, 9882.62, 16.66],
        ["HourBreakout_USDJPY", 4, "2013-03-06", "2013-03-08", 1, "Passed", "Profit Target", 2, 8379.14, 9382.56, 7379.14, 9179.14, 114.91],
        ["HourBreakout_USDJPY", 4, "2013-03-08", "2013-03-15", 2, "Passed", "Profit Target", 6, 9382.56, 9907.99, 8382.56, 9882.56, 15.95],
        ["HourBreakout_GBPUSD", 1, "2013-03-05", "2013-03-19", 3, "Payout", "Payout", 14, 12293.68, 12697.61, 11293.68, 12693.68, 0.0],
        ["HourBreakout_USDJPY", 4, "2013-03-15", "2013-03-29", 3, "Payout", "Payout", 14, 9907.99, 10313.63, 8907.99, 10307.99, 0.0],
    ]

    columns = [
        "Strategy_Pair",
        "Challenge Number",
        "Start Phase Date",
        "End Phase Date",
        "Phase",
        "Outcome",
        "Reason",
        "Duration",
        "Start Balance",
        "Ending Balance",
        "Max Drawdown",
        "Profit Target",
        "Daily Drawdown"
    ]

    df_funded_joined = pd.DataFrame(data, columns=columns)

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
        "phase1": empty_df,
        "phase2": empty_df,
        "phase3": empty_df,
        "challenge": empty_df,
        "funded": df_funded_joined
    }

    calculator = MetricsCalculator(dfs)
    results = calculator.calculate_metrics()
    f = results["funded"]

    #assert f["f_number_challenges"] == 0
    #assert f["f_number_passed_challenges"] == 0
    #assert f["f_number_failed_challenges"] == 0
    #assert f["f_challenge_winrate"] == 0
    #assert f["f_average_challenge_duration"] == 0
    #assert f["f_average_challenge_passed_duration"] == 0
    #assert f["f_average_challenge_failed_duration"] == 0
    #assert f["f_max_cons_challenge_passed"] == 0
    #assert f["f_max_cons_challenge_failed"] == 0
    #assert f["f_average_cons_challenge_passed"] == 0
    #assert f["f_average_cons_challenge_failed"] == 0
    #assert f["f_average_profit_challenge"] == 0
    #assert f["f_challenge_efficiency_ratio"] == 0
    #assert f["f_payout_winrate"] == 0
    #assert f["f_max_cons_payouts"] == 0
    #assert f["f_average_payouts_challenge"] == 0
    #assert f["f_average_profit_payout"] == 0
    #assert f["f_profitability_ratio"] == 0