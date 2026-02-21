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
        p1_efficiency_ratio = round(p1_challenge_winrate / p1_average_challenge_duration, 2)

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
        df["Duration"] = df["Duration"].astype(float)
        df["Start Balance"] = df["Start Balance"].astype(float)
        df["Ending Balance"] = df["Ending Balance"].astype(float)
        outcome_series = df["Outcome"] 
        passed_group = self._calculate_consecutive_metrics(outcome_series, "Payout")
        failed_group = self._calculate_consecutive_metrics(outcome_series, "Failed")
        payout_rows = df[df["Outcome"] == "Payout"].copy()
        payout_rows["Payout Amount"] = payout_rows["Ending Balance"] - payout_rows["Start Balance"]
        cost_per_challenge = 80

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
        df["Outcome"] = df["Outcome"].astype(str).str.strip()
        df["Phase"] = pd.to_numeric(df["Phase"], errors = "coerce").fillna(0).astype(int)
        df["Duration"] = pd.to_numeric(df["Duration"], errors = "coerce").fillna(0)

        #Group all phases by challenge
        challenge_groups = df.groupby("Challenge Number")
        challenge_records = []
        failed_p1_count = failed_p2_count = 0

        for (keys), group in challenge_groups:
            p1 = group[group["Phase"] == 1]
            p2 = group[group["Phase"] == 2]
            total_duration = group["Duration"].sum()

            if not p2.empty:
                completion_row = p2["_row_index"].min()
            else:
                completion_row = p1["_row_index"].min() if not p1.empty else group["_row_index"].min()
            
            if (not p1.empty and not p2.empty
                and p1["Outcome"].iloc[0] == "Passed"
                and p2["Outcome"].iloc[0] == "Passed"):
                outcome = "Passed"
            else:
                outcome = "Failed"
                if not p1.empty and p1["Outcome"].iloc[0] == "Failed":
                    failed_p1_count += 1
                elif not p2.empty and p2["Outcome"].iloc[0] == "Failed":
                    failed_p2_count += 1
                else:
                    failed_p1_count += 1
            
            challenge_records.append({
                "keys": keys,
                "Outcome": outcome,
                "Duration": total_duration,
                "completion_row": completion_row
            })

        # sort by actual completion order
        challenge_df = pd.DataFrame(challenge_records).sort_values("completion_row").reset_index(drop=True)

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
        df = self.dfs["funded"]
        df["Outcome"] = df["Outcome"].astype(str).str.strip()
        df["Phase"] = pd.to_numeric(df["Phase"], errors = "coerce").fillna(0).astype(int)
        df["Duration"] = pd.to_numeric(df["Duration"], errors = "coerce").fillna(0)
        df["Start Balance"] = pd.to_numeric(df["Start Balance"], errors = "coerce").fillna(0)
        df["Ending Balance"] = pd.to_numeric(df["Ending Balance"], errors = "coerce").fillna(0)

        challenge_groups = df.groupby(["Challenge Number"])
        f_number_challenges = challenge_groups.ngroups
        f_number_passed_challenges = total_payouts = f_number_failed_challenges = 0
        challenge_durations = []
        passed_durations = []
        failed_durations = []
        challenge_outcomes = []
        payout_profits = []

        # process each challenge
        for _, group in challenge_groups:
            group = group.sort_values("Phase")
            payouts = group[group["Outcome"] == "Payout"]
            total_duration = group["Duration"].sum()
            challenge_durations.append(total_duration)

            if not payouts.empty:
                f_number_passed_challenges += 1
                total_payouts += len(payouts)
                passed_durations.append(total_duration)
                challenge_outcomes.append("Payout")
                payout_profits.extend((payouts["Ending Balance"] - payouts["Start Balance"]).tolist())
            else:
                f_number_failed_challenges += 1
                failed_durations.append(total_duration)
                challenge_outcomes.append("Failed")

        f_challenge_winrate = round((f_number_passed_challenges / f_number_challenges) * 100, 2) if f_number_challenges else 0
        f_payout_winrate = round((total_payouts / (total_payouts + f_number_failed_challenges)) * 100, 2) if (total_payouts + f_number_failed_challenges) else 0
        f_average_challenge_duration = round(sum(challenge_durations) / len(challenge_durations), 2) if challenge_durations else 0
        f_average_challenge_passed_duration = round(sum(passed_durations) / len(passed_durations), 2) if passed_durations else 0
        f_average_challenge_failed_duration = round(sum(failed_durations) / len(failed_durations), 2) if failed_durations else 0

        if challenge_outcomes:
            series = pd.Series(challenge_outcomes)
            groups = (series != series.shift()).cumsum()
            streaks = series.groupby(groups).agg(['first', 'size'])
            win_streaks = streaks[streaks['first'] == 'Payout']["size"]
            loss_streaks = streaks[streaks['first'] == 'Failed']["size"]
            f_max_cons_challenge_passed = int(win_streaks.max()) if not win_streaks.empty else 0
            f_max_cons_challenge_failed = int(loss_streaks.max()) if not loss_streaks.empty else 0
            f_average_cons_challenge_passed = round(win_streaks.mean(), 2) if not win_streaks.empty else 0
            f_average_cons_challenge_failed = round(loss_streaks.mean(), 2) if not loss_streaks.empty else 0
        else:
            f_max_cons_challenge_passed = f_max_cons_challenge_failed = f_average_cons_challenge_failed = f_average_cons_challenge_passed = 0

        df_sorted = df.sort_values(["Challenge Number", "Phase"])
        all_payout_series = (df_sorted["Outcome"] == "Payout").astype(int)
        streak_groups = (all_payout_series != all_payout_series.shift()).cumsum()
        streaks = all_payout_series.groupby(streak_groups).sum()
        all_challenge_payout_streaks = streaks[streaks > 0].tolist()
        f_max_cons_payouts = max(all_challenge_payout_streaks) if all_challenge_payout_streaks else 0
        f_average_payouts_challenge = round(sum(all_challenge_payout_streaks) / len(all_challenge_payout_streaks), 2) if all_challenge_payout_streaks else 0

        f_average_profit_payout = round(sum(payout_profits) / len(payout_profits), 2) if payout_profits else 0
        total_challenge_profits = []
        for _, group in df.groupby("Challenge Number"):
            payouts = group[group["Outcome"] == "Payout"]
            total_profit = (payouts["Ending Balance"] - payouts["Start Balance"]).sum() if not payouts.empty else -80
            total_challenge_profits.append(total_profit)
        f_average_profit_challenge = round(sum(total_challenge_profits) / len(total_challenge_profits), 2) if total_challenge_profits else 0

        df["End Phase Date"] = pd.to_datetime(df["End Phase Date"], errors = "coerce")
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
        f_profitability_ratio = round(((f_payout_winrate / 100) * f_average_payouts_challenge * f_average_profit_payout) / 80, 2)
        if m_average_monthly_loss != 0: m_monthly_stability_return_ratio = round(((m_monthly_winrate / 100) * m_average_monthly_profit) / abs(m_average_monthly_loss),2) 
        else: m_monthly_stability_return_ratio = 0
        if f_number_failed_challenges != 0: f_challenge_efficiency_ratio = round(f_average_profit_challenge / f_number_failed_challenges, 2) 
        else: f_challenge_efficiency_ratio = 0
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