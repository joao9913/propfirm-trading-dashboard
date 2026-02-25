import pandas as pd
import numpy as np

class MetricsCalculator:
    def __init__(self, dfs):
        self.dfs = dfs
    
    def calculate_metrics(self):
        dispatch_types = {
            "phase1": self._calculate_metrics_phase1_2("phase1"),
            "phase2": self._calculate_metrics_phase1_2("phase2"),
            "phase3": self._calculate_metrics_phase3(),
            "challenge": self._calculate_metrics_challenge(),
            "funded": self._calculate_metrics_funded(),
        }

        return dispatch_types

    #Private methods for calculating metrics depending on phase
    def _calculate_metrics_phase1_2(self, phasename: str):
        df = self.dfs[phasename]
        prefix = "p1" if phasename == "phase1" else "p2" if phasename == "phase2" else None

        if df.empty:
            return{
                prefix + "_number_passed_challenges": 0,
                prefix + "_number_failed_challenges": 0,
                prefix + "_number_challenges": 0,
                prefix + "_challenge_winrate": 0,
                prefix + "_average_challenge_duration": 0,
                prefix + "_average_challenge_passed_duration": 0,
                prefix + "_average_challenge_failed_duration": 0,
                prefix + "_max_cons_challenge_passed": 0,
                prefix + "_max_cons_challenge_failed": 0,
                prefix + "_average_cons_challenge_passed": 0,
                prefix + "_average_cons_challenge_failed": 0,
                prefix + "_efficiency_ratio": 0,
            }

        df["Duration"] = df["Duration"].astype(float)
        outcome_series = df["Outcome"]
        passed_group = self._calculate_consecutive_metrics(outcome_series, "Passed")
        failed_group = self._calculate_consecutive_metrics(outcome_series, "Failed")

        p1_number_passed_challenges = (outcome_series == "Passed").sum()
        p1_number_failed_challenges = (outcome_series == "Failed").sum()
        p1_number_challenges = p1_number_failed_challenges + p1_number_passed_challenges
        p1_challenge_winrate = round((p1_number_passed_challenges / p1_number_challenges) * 100, 2) if p1_number_challenges else 0
        p1_average_challenge_duration = round(df["Duration"].mean(), 2) if p1_number_challenges else 0
        p1_average_challenge_passed_duration = round(df[outcome_series == "Passed"]["Duration"].mean(), 2)
        p1_average_challenge_failed_duration = round(df[outcome_series == "Failed"]["Duration"].mean(), 2)
        p1_max_cons_challenge_passed = passed_group.max() if not passed_group.empty else 0
        p1_max_cons_challenge_failed = failed_group.max() if not failed_group.empty else 0
        p1_average_cons_challenge_passed = round(passed_group.mean(), 2) if not passed_group.empty else 0
        p1_average_cons_challenge_failed = round(failed_group.mean(), 2) if not failed_group.empty else 0
        p1_efficiency_ratio = round(
            (p1_challenge_winrate / p1_average_challenge_duration) if p1_average_challenge_duration else 0,
            2
        )

        metrics_dict = {
            prefix + "_number_passed_challenges": p1_number_passed_challenges,
            prefix + "_number_failed_challenges": p1_number_failed_challenges,
            prefix + "_number_challenges": p1_number_challenges,
            prefix + "_challenge_winrate": p1_challenge_winrate,
            prefix + "_average_challenge_duration": p1_average_challenge_duration,
            prefix + "_average_challenge_passed_duration": p1_average_challenge_passed_duration,
            prefix + "_average_challenge_failed_duration": p1_average_challenge_failed_duration,
            prefix + "_max_cons_challenge_passed": p1_max_cons_challenge_passed,
            prefix + "_max_cons_challenge_failed": p1_max_cons_challenge_failed,
            prefix + "_average_cons_challenge_passed": p1_average_cons_challenge_passed,
            prefix + "_average_cons_challenge_failed": p1_average_cons_challenge_failed,
            prefix + "_efficiency_ratio": p1_efficiency_ratio,
        }

        return metrics_dict
        
    def _calculate_metrics_phase3(self):
        df = self.dfs["phase3"]
        
        if df.empty:
            return{
                "p3_number_payouts": 0,
                "p3_number_failed_challenges": 0,
                "p3_number_challenges": 0,
                "p3_payout_winrate": 0,
                "p3_average_challenge_duration": 0,
                "p3_average_challenge_passed_duration": 0,
                "p3_average_challenge_failed_duration": 0,
                "p3_max_cons_payouts": 0,
                "p3_max_cons_failed": 0,
                "p3_average_max_cons_payouts": 0,
                "p3_average_max_cons_failed": 0,
                "p3_average_profit_payout": 0,
                "p3_total_profit_payouts": 0,
                "p3_total_loss_payouts": 0,
                "p3_profit_factor": 0,
                "p3_profitability_ratio": 0,
            }

        df["Duration"] = df["Duration"].astype(float)
        df["Start Balance"] = df["Start Balance"].astype(float)
        df["Ending Balance"] = df["Ending Balance"].astype(float)
        outcome_series = df["Outcome"] 
        passed_group = self._calculate_consecutive_metrics(outcome_series, "Payout")
        failed_group = self._calculate_consecutive_metrics(outcome_series, "Failed")
        payout_rows = df[df["Outcome"] == "Payout"].copy()
        payout_rows["Payout Amount"] = payout_rows["Ending Balance"] - payout_rows["Start Balance"]
        cost_per_challenge = 80

        df["PnL"] = np.where(
            df["Outcome"] == "Payout",
            df["Ending Balance"] - df["Start Balance"],
            np.where(df["Outcome"] == "Failed", -cost_per_challenge, 0)
        )

        p3_number_payouts = (outcome_series == "Payout").sum()
        p3_number_failed_challenges = (outcome_series == "Failed").sum()
        p3_number_challenges = p3_number_failed_challenges + p3_number_payouts
        p3_payout_winrate = round((p3_number_payouts / p3_number_challenges) * 100, 2) if p3_number_challenges else 0
        p3_average_challenge_duration = round(df["Duration"].mean(), 2) if p3_number_challenges else 0
        p3_average_challenge_passed_duration = round(df[outcome_series == "Payout"]["Duration"].mean(), 2) if p3_number_payouts else 0
        p3_average_challenge_failed_duration = round(df[outcome_series == "Failed"]["Duration"].mean(), 2) if p3_number_failed_challenges else 0
        p3_max_cons_payouts = passed_group.max() if not passed_group.empty else 0
        p3_max_cons_failed = failed_group.max() if not failed_group.empty else 0
        p3_average_max_cons_payouts = round(passed_group.mean(), 2) if not passed_group.empty else 0
        p3_average_max_cons_failed = round(failed_group.mean(), 2) if not failed_group.empty else 0
        p3_average_profit_payout = round(payout_rows["Payout Amount"].mean(), 2) if not payout_rows.empty else 0
        p3_total_profit_payouts = round(payout_rows["Payout Amount"].sum(), 2) if not payout_rows.empty else 0
        p3_total_loss_payouts = p3_number_failed_challenges * cost_per_challenge
        p3_profit_factor = round(p3_total_profit_payouts / p3_total_loss_payouts, 2) if p3_total_loss_payouts != 0 else float('inf')
        p3_profitability_ratio = round(((p3_payout_winrate / 100 * p3_average_profit_payout) / cost_per_challenge) * 10, 2)

        metrics_dict = {
            "p3_number_payouts": p3_number_payouts,
            "p3_number_failed_challenges": p3_number_failed_challenges,
            "p3_number_challenges": p3_number_challenges,
            "p3_payout_winrate": p3_payout_winrate,
            "p3_average_challenge_duration": p3_average_challenge_duration,
            "p3_average_challenge_passed_duration": p3_average_challenge_passed_duration,
            "p3_average_challenge_failed_duration": p3_average_challenge_failed_duration,
            "p3_max_cons_payouts": p3_max_cons_payouts,
            "p3_max_cons_failed": p3_max_cons_failed,
            "p3_average_max_cons_payouts": p3_average_max_cons_payouts,
            "p3_average_max_cons_failed": p3_average_max_cons_failed,
            "p3_average_profit_payout": p3_average_profit_payout,
            "p3_total_profit_payouts": p3_total_profit_payouts,
            "p3_total_loss_payouts": p3_total_loss_payouts,
            "p3_profit_factor": p3_profit_factor,
            "p3_profitability_ratio": p3_profitability_ratio,
        }

        return metrics_dict
    
    def _calculate_metrics_challenge(self):
        df = self.dfs["challenge"].reset_index(drop = False).rename(columns={"index": "_row_index"})

        if df.empty:
            return{
                "c_number_challenges": 0,
                "c_number_passed_challenges": 0,
                "c_number_failed_challenges": 0,
                "c_challenge_winrate": 0,
                "c_average_challenge_duration": 0,
                "c_average_challenge_passed_duration": 0,
                "c_average_challenge_failed_duration": 0,
                "c_max_cons_challenge_passed": 0,
                "c_max_cons_challenge_failed": 0,
                "c_average_cons_challenge_passed": 0,
                "c_average_cons_challenge_failed": 0,
                "c_failed_p1_percentage": 0,
                "c_failed_p2_percentage": 0,
                "c_efficiency_ratio": 0
            }

        df["Outcome"] = df["Outcome"].astype(str).str.strip()
        df["Phase"] = pd.to_numeric(df["Phase"], errors = "coerce").fillna(0).astype(int)
        df["Duration"] = pd.to_numeric(df["Duration"], errors = "coerce").fillna(0)

        #Group all phases by challenge and by strategies
        if "Strategy_Pair" not in df.columns:
            df["Strategy_Pair"] = "Single_Run"

        challenge_records = []
        for strategy, strategy_df in df.groupby("Strategy_Pair"):
            for challenge_num, group in strategy_df.groupby("Challenge Number"):
                p1 = group[group["Phase"] == 1]
                p2 = group[group["Phase"] == 2]
                total_duration = group["Duration"].sum()

                if not p2.empty:
                    completion_row = p2["_row_index"].min()
                else:
                    completion_row = p1["_row_index"].min() if not p1.empty else group["_row_index"].min()

                if not p1.empty and not p2.empty and p1["Outcome"].iloc[0] == "Passed" and p2["Outcome"].iloc[0] == "Passed":
                    outcome = "Passed"
                else:
                    outcome = "Failed"
                
                challenge_records.append({
                    "Strategy_Pair": strategy,
                    "Challenge Number": challenge_num,
                    "Outcome": outcome,
                    "Duration": total_duration,
                    "completion_row": completion_row
                })

        # sort by actual completion order
        challenge_df = pd.DataFrame(challenge_records).sort_values("completion_row").reset_index(drop=True)

        failed_challenges = df[df["Outcome"] == "Failed"]
        failed_p1_count = failed_challenges[failed_challenges["Phase"] == 1]["Challenge Number"].nunique()
        failed_p2_count = failed_challenges[failed_challenges["Phase"] == 2]["Challenge Number"].nunique()
        
        # consecutive streaks based on chronological completion
        series = challenge_df["Outcome"]
        groups = (series != series.shift()).cumsum()
        streaks = series.groupby(groups).agg(["first", "size"])
        win_streaks = streaks[streaks["first"] == "Passed"]["size"]
        loss_streaks = streaks[streaks["first"] == "Failed"]["size"]

        # metrics
        c_number_challenges = len(challenge_df)
        c_number_passed_challenges = (challenge_df["Outcome"] == "Passed").sum()
        c_number_failed_challenges = (challenge_df["Outcome"] == "Failed").sum()
        c_challenge_winrate = round((c_number_passed_challenges / c_number_challenges) * 100, 2) if c_number_challenges else 0
        c_average_challenge_duration = round(challenge_df["Duration"].mean(), 2) if c_number_challenges else 0
        c_average_challenge_passed_duration = round(challenge_df[challenge_df["Outcome"] == "Passed"]["Duration"].mean(), 2) if c_number_passed_challenges else 0
        c_average_challenge_failed_duration = round(challenge_df[challenge_df["Outcome"] == "Failed"]["Duration"].mean(), 2) if c_number_failed_challenges else 0
        c_max_cons_challenge_passed = int(win_streaks.max()) if not win_streaks.empty else 0
        c_max_cons_challenge_failed = int(loss_streaks.max()) if not loss_streaks.empty else 0
        c_average_cons_challenge_passed = round(win_streaks.mean(), 2) if not win_streaks.empty else 0
        c_average_cons_challenge_failed = round(loss_streaks.mean(), 2) if not loss_streaks.empty else 0
        c_failed_p1_percentage = round((failed_p1_count / c_number_failed_challenges) * 100, 2) if c_number_failed_challenges else 0
        c_failed_p2_percentage = round((failed_p2_count / c_number_failed_challenges) * 100, 2) if c_number_failed_challenges else 0
        c_efficiency_ratio = round(c_challenge_winrate / c_average_challenge_duration, 2)

        metrics_dict = {
            "c_number_challenges": c_number_challenges,
            "c_number_passed_challenges": c_number_passed_challenges,
            "c_number_failed_challenges": c_number_failed_challenges,
            "c_challenge_winrate": c_challenge_winrate,
            "c_average_challenge_duration": c_average_challenge_duration,
            "c_average_challenge_passed_duration": c_average_challenge_passed_duration,
            "c_average_challenge_failed_duration": c_average_challenge_failed_duration,
            "c_max_cons_challenge_passed": c_max_cons_challenge_passed,
            "c_max_cons_challenge_failed": c_max_cons_challenge_failed,
            "c_average_cons_challenge_passed": c_average_cons_challenge_passed,
            "c_average_cons_challenge_failed": c_average_cons_challenge_failed,
            "c_failed_p1_percentage": c_failed_p1_percentage,
            "c_failed_p2_percentage": c_failed_p2_percentage,
            "c_efficiency_ratio": c_efficiency_ratio
        }

        return metrics_dict

    def _calculate_metrics_funded(self):
        import pandas as pd
        import numpy as np

        df = self.dfs["funded"]

        if "Strategy_Pair" not in df.columns:
            df["Strategy_Pair"] = "Single_Run"

        if df.empty:
            return {
                "f_number_challenges": 0,
                "f_number_passed_challenges": 0,
                "f_number_failed_challenges": 0,
                "f_challenge_winrate": 0,
                "f_payout_winrate": 0,
                "f_average_challenge_duration": 0,
                "f_average_challenge_passed_duration": 0,
                "f_average_challenge_failed_duration": 0,
                "f_max_cons_challenge_passed": 0,
                "f_max_cons_challenge_failed": 0,
                "f_average_cons_challenge_passed": 0,
                "f_average_cons_challenge_failed": 0,
                "f_max_cons_payouts": 0,
                "f_average_payouts_challenge": 0,
                "f_average_profit_payout": 0,
                "f_average_profit_challenge": 0,
                "m_winning_months": 0,
                "m_losing_months": 0,
                "m_monthly_winrate": 0,
                "m_average_monthly_profit": 0,
                "m_average_monthly_loss": 0,
                "m_monthly_wl_ratio": 0,
                "f_challenge_efficiency_ratio": 0,
                "m_overall_risk_adjusted_returns": 0,
                "f_profitability_ratio": 0,
                "m_monthly_stability_return_ratio": 0
            }

        # Clean data
        df["Outcome"] = df["Outcome"].astype(str).str.strip()
        df["Phase"] = pd.to_numeric(df["Phase"], errors="coerce").fillna(0).astype(int)
        df["Duration"] = pd.to_numeric(df["Duration"], errors="coerce").fillna(0)
        df["Start Balance"] = pd.to_numeric(df["Start Balance"], errors="coerce").fillna(0)
        df["Ending Balance"] = pd.to_numeric(df["Ending Balance"], errors="coerce").fillna(0)
        df["End Phase Date"] = pd.to_datetime(df["End Phase Date"], errors="coerce")

        # Group by strategy and challenge
        challenge_groups = df.groupby(["Strategy_Pair", "Challenge Number"])
        f_number_challenges = challenge_groups.ngroups
        f_number_passed_challenges = total_payouts = f_number_failed_challenges = 0
        challenge_durations = []
        passed_durations = []
        failed_durations = []
        payout_profits = []
        challenge_records = []

        # Process each challenge
        for (strategy, challenge_num), group in challenge_groups:
            group = group.sort_values("Phase")
            p1 = group[group["Phase"] == 1]
            p2 = group[group["Phase"] == 2]
            payouts = group[group["Outcome"] == "Payout"]

            base_duration = p1["Duration"].sum() + p2["Duration"].sum()

            # Determine resolution date properly
            if not payouts.empty:
                first_payout = payouts.iloc[0]
                total_duration = base_duration + first_payout["Duration"]
                outcome = "Passed"
                f_number_passed_challenges += 1
                total_payouts += len(payouts)
                passed_durations.append(total_duration)
                payout_profits.extend((payouts["Ending Balance"] - payouts["Start Balance"]).tolist())
                resolution_date = first_payout["End Phase Date"]
            else:
                total_duration = group["Duration"].sum()
                outcome = "Failed"
                f_number_failed_challenges += 1
                failed_durations.append(total_duration)
                resolution_date = group["End Phase Date"].max()

            challenge_durations.append(total_duration)
            challenge_records.append({
                "Strategy_Pair": strategy,
                "Challenge Number": challenge_num,
                "Outcome": outcome,
                "Duration": total_duration,
                "Resolution_Date": resolution_date
            })

        # Create challenge dataframe for chronological streaks
        challenge_df = pd.DataFrame(challenge_records)
        challenge_df = challenge_df.sort_values("Resolution_Date").reset_index(drop=True)

        # Win/Loss streaks across all strategies chronologically
        max_passed = max_failed = 0
        current_passed = current_failed = 0
        for outcome in challenge_df["Outcome"]:
            if outcome == "Passed":
                current_passed += 1
                current_failed = 0
            else:
                current_failed += 1
                current_passed = 0
            max_passed = max(max_passed, current_passed)
            max_failed = max(max_failed, current_failed)

        f_max_cons_challenge_passed = max_passed
        f_max_cons_challenge_failed = max_failed

        # Average consecutive passed/failed
        # Recalculate properly
        streaks = []
        current = 0
        last_outcome = None
        for outcome in challenge_df["Outcome"]:
            if outcome == last_outcome:
                current += 1
            else:
                if last_outcome is not None:
                    streaks.append((last_outcome, current))
                current = 1
                last_outcome = outcome
        if last_outcome is not None:
            streaks.append((last_outcome, current))
        win_streaks = [s for o, s in streaks if o == "Passed"]
        loss_streaks = [s for o, s in streaks if o == "Failed"]
        f_average_cons_challenge_passed = round(np.mean(win_streaks), 2) if win_streaks else 0
        f_average_cons_challenge_failed = round(np.mean(loss_streaks), 2) if loss_streaks else 0

        # Challenge-level metrics
        f_challenge_winrate = round((f_number_passed_challenges / f_number_challenges) * 100, 2) if f_number_challenges else 0
        f_payout_winrate = round((total_payouts / (total_payouts + f_number_failed_challenges)) * 100, 2) if (total_payouts + f_number_failed_challenges) else 0
        f_average_challenge_duration = round(sum(challenge_durations) / len(challenge_durations), 2) if challenge_durations else 0
        f_average_challenge_passed_duration = round(sum(passed_durations) / len(passed_durations), 2) if passed_durations else 0
        f_average_challenge_failed_duration = round(sum(failed_durations) / len(failed_durations), 2) if failed_durations else 0

        # Payout streaks
        df_sorted = df.sort_values(["Strategy_Pair", "Challenge Number", "Phase"])
        all_payout_series = (df_sorted["Outcome"] == "Payout").astype(int)
        streak_groups = (all_payout_series != all_payout_series.shift()).cumsum()
        streaks = all_payout_series.groupby(streak_groups).sum()
        all_challenge_payout_streaks = streaks[streaks > 0].tolist()
        f_max_cons_payouts = max(all_challenge_payout_streaks) if all_challenge_payout_streaks else 0
        f_average_payouts_challenge = round(sum(all_challenge_payout_streaks) / len(all_challenge_payout_streaks), 2) if all_challenge_payout_streaks else 0

        # Profit metrics
        f_average_profit_payout = round(sum(payout_profits) / len(payout_profits), 2) if payout_profits else 0
        total_challenge_profits = []
        for _, group in df.groupby(["Strategy_Pair", "Challenge Number"]):
            payouts = group[group["Outcome"] == "Payout"]
            total_profit = (payouts["Ending Balance"] - payouts["Start Balance"]).sum() if not payouts.empty else -80
            total_challenge_profits.append(total_profit)
        f_average_profit_challenge = round(sum(total_challenge_profits) / len(total_challenge_profits), 2) if total_challenge_profits else 0

        # Monthly metrics
        df["PnL"] = np.where(
            df["Outcome"] == "Payout",
            df["Ending Balance"] - df["Start Balance"],
            np.where(df["Outcome"] == "Failed", -80, 0)
        )
        df["Month"] = df["End Phase Date"].dt.to_period("M").astype(str)
        m_average_monthly_pnl = df.groupby("Month")["PnL"].sum()
        m_winning_months = int((m_average_monthly_pnl > 0).sum())
        m_losing_months = int((m_average_monthly_pnl < 0).sum())
        m_monthly_winrate = round((m_winning_months / (m_winning_months + m_losing_months)) * 100, 2) if (m_winning_months + m_losing_months) else 0
        m_average_monthly_profit = round(m_average_monthly_pnl[m_average_monthly_pnl > 0].mean(), 2) if (m_average_monthly_pnl > 0).any() else 0
        m_average_monthly_loss = round(m_average_monthly_pnl[m_average_monthly_pnl < 0].mean(), 2) if (m_average_monthly_pnl < 0).any() else 0
        m_monthly_wl_ratio = round(m_winning_months / m_losing_months, 2) if m_losing_months > 0 else float('inf')

        # Ratios
        f_profitability_ratio = round(((f_payout_winrate / 100) * f_average_payouts_challenge * f_average_profit_payout) / 80, 2)
        m_monthly_stability_return_ratio = round(((m_monthly_winrate / 100) * m_average_monthly_profit) / abs(m_average_monthly_loss), 2) if m_average_monthly_loss != 0 else 0
        f_challenge_efficiency_ratio = round(f_average_profit_challenge / f_number_failed_challenges, 2) if f_number_failed_challenges != 0 else 0
        m_overall_risk_adjusted_returns = round(f_challenge_efficiency_ratio * m_monthly_stability_return_ratio, 2)

        metrics_dict = {
            "f_number_challenges": f_number_challenges,
            "f_number_passed_challenges": f_number_passed_challenges,
            "f_number_failed_challenges": f_number_failed_challenges,
            "f_challenge_winrate": f_challenge_winrate,
            "f_payout_winrate": f_payout_winrate,
            "f_average_challenge_duration": f_average_challenge_duration,
            "f_average_challenge_passed_duration": f_average_challenge_passed_duration,
            "f_average_challenge_failed_duration": f_average_challenge_failed_duration,
            "f_max_cons_challenge_passed": f_max_cons_challenge_passed,
            "f_max_cons_challenge_failed": f_max_cons_challenge_failed,
            "f_average_cons_challenge_passed": f_average_cons_challenge_passed,
            "f_average_cons_challenge_failed": f_average_cons_challenge_failed,
            "f_max_cons_payouts": f_max_cons_payouts,
            "f_average_payouts_challenge": f_average_payouts_challenge,
            "f_average_profit_payout": f_average_profit_payout,
            "f_average_profit_challenge": f_average_profit_challenge,
            "m_winning_months": m_winning_months,
            "m_losing_months": m_losing_months,
            "m_monthly_winrate": m_monthly_winrate,
            "m_average_monthly_profit": m_average_monthly_profit,
            "m_average_monthly_loss": m_average_monthly_loss,
            "m_monthly_wl_ratio": m_monthly_wl_ratio,
            "f_challenge_efficiency_ratio": f_challenge_efficiency_ratio,
            "m_overall_risk_adjusted_returns": m_overall_risk_adjusted_returns,
            "f_profitability_ratio": f_profitability_ratio,
            "m_monthly_stability_return_ratio": m_monthly_stability_return_ratio
        }

        return metrics_dict
    
    def _calculate_consecutive_metrics(self, series, outcome):
        mask = series == outcome
        streaks = mask.groupby((mask != mask.shift()).cumsum()).sum()
        streaks = streaks[streaks > 0]
        return streaks