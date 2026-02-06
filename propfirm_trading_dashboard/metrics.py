import pandas as pd
import numpy as np

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
        passed_group = self._calculate_consecutive_metrics(outcome_series, "Passed")
        failed_group = self._calculate_consecutive_metrics(outcome_series, "Failed")

        number_passed = (outcome_series == "Passed").sum()
        number_failed = (outcome_series == "Failed").sum()
        total_outcomes = number_failed + number_passed
        winrate = round((number_passed / total_outcomes) * 100, 2) if total_outcomes else 0
        average_duration = round(self.df["Duration"].mean(), 2) if total_outcomes else 0
        average_duration_passed = round(self.df[outcome_series == "Passed"]["Duration"].mean(), 2)
        average_duration_failed = round(self.df[outcome_series == "Failed"]["Duration"].mean(), 2)
        max_cons_wins = passed_group.max() if not passed_group.empty else 0
        max_cons_losses = failed_group.max() if not failed_group.empty else 0
        average_cons_wins = round(passed_group.mean(), 2) if not passed_group.empty else 0
        average_cons_losses = round(failed_group.mean(), 2) if not failed_group.empty else 0
        efficiency_ratio = round(winrate / average_duration, 2)

        metrics_dict = {
            "Number Passed": number_passed,
            "Number Failed": number_failed,
            "Total Outcomes": total_outcomes,
            "Winrate": winrate,
            "Average Duration": average_duration,
            "Average Duration Passed": average_duration_passed,
            "Average Duration Failed": average_duration_failed,
            "Max Consecutive Passed": max_cons_wins,
            "Max Consecutive Losses": max_cons_losses,
            "Average Consecutive Passed": average_cons_wins,
            "Average Consecutive Failed": average_cons_losses,
            "Efficiency Ratio": efficiency_ratio,
        }

        return metrics_dict
        
    def _calculate_metrics_phase3(self):
        self.df["Duration"] = self.df["Duration"].astype(float)
        self.df["Start Balance"] = self.df["Start Balance"].astype(float)
        self.df["Ending Balance"] = self.df["Ending Balance"].astype(float)
        outcome_series = self.df["Outcome"] 
        passed_group = self._calculate_consecutive_metrics(outcome_series, "Payout")
        failed_group = self._calculate_consecutive_metrics(outcome_series, "Failed")
        payout_rows = self.df[self.df["Outcome"] == "Payout"].copy()
        payout_rows["Payout Amount"] = payout_rows["Ending Balance"] - payout_rows["Start Balance"]
        cost_per_challenge = 80

        number_payouts = (outcome_series == "Payout").sum()
        number_failed = (outcome_series == "Failed").sum()
        total_outcomes = number_failed + number_payouts
        winrate = round((number_payouts / total_outcomes) * 100, 2) if total_outcomes else 0
        average_duration = round(self.df["Duration"].mean(), 2) if total_outcomes else 0
        average_payout_duration = round(self.df[outcome_series == "Payout"]["Duration"].mean(), 2) if number_payouts else 0
        average_failed_duration = round(self.df[outcome_series == "Failed"]["Duration"].mean(), 2) if number_failed else 0
        max_cons_payouts = passed_group.max() if not passed_group.empty else 0
        max_cons_losses = failed_group.max() if not failed_group.empty else 0
        average_cons_payouts = round(passed_group.mean(), 2) if not passed_group.empty else 0
        average_cons_losses = round(failed_group.mean(), 2) if not failed_group.empty else 0
        average_per_payout = round(payout_rows["Payout Amount"].mean(), 2) if not payout_rows.empty else 0
        total_profit_payouts = round(payout_rows["Payout Amount"].sum(), 2) if not payout_rows.empty else 0
        total_gross_loss = number_failed * cost_per_challenge
        profit_factor = round(total_profit_payouts / total_gross_loss, 2) if total_gross_loss != 0 else float('inf')
        profitability_ratio = round(((winrate / 100 * average_per_payout) / cost_per_challenge) * 10, 2)

        metrics_dict = {
            "Number Payouts": number_payouts,
            "Number Failed": number_failed,
            "Total Outcomes": total_outcomes,
            "Winrate": winrate,
            "Average Duration": average_duration,
            "Average Duration Payout": average_payout_duration,
            "Average Duration Failed": average_failed_duration,
            "Max Consecutive Payouts": max_cons_payouts,
            "Max Consecutive Losses": max_cons_losses,
            "Average Consecutive Payouts": average_cons_payouts,
            "Average Consecutive Failed": average_cons_losses,
            "Average Profit Per Payout": average_per_payout,
            "Total Profit Payouts": total_profit_payouts,
            "Total Gross Loss": total_gross_loss,
            "Profit Factor": profit_factor,
            "Profitability Ratio": profitability_ratio,
        }

        return metrics_dict
    
    def _calculate_metrics_challenge(self):
        df = self.df.copy().reset_index(drop = False).rename(columns={"index": "_row_index"})
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
        total_challenges = len(challenge_df)
        total_passed_challenges = (challenge_df["Outcome"] == "Passed").sum()
        total_failed_challenges = (challenge_df["Outcome"] == "Failed").sum()
        winrate = round((total_passed_challenges / total_challenges) * 100, 2) if total_challenges else 0
        average_duration_challenge = round(challenge_df["Duration"].mean(), 2) if total_challenges else 0
        average_duration_passed = round(challenge_df[challenge_df["Outcome"] == "Passed"]["Duration"].mean(), 2) if total_passed_challenges else 0
        average_duration_failed = round(challenge_df[challenge_df["Outcome"] == "Failed"]["Duration"].mean(), 2) if total_failed_challenges else 0
        max_cons_wins = int(win_streaks.max()) if not win_streaks.empty else 0
        max_cons_losses = int(loss_streaks.max()) if not loss_streaks.empty else 0
        average_cons_wins = round(win_streaks.mean(), 2) if not win_streaks.empty else 0
        average_cons_losses = round(loss_streaks.mean(), 2) if not loss_streaks.empty else 0
        failed_p1_percentage = round((failed_p1_count / total_failed_challenges) * 100, 2) if total_failed_challenges else 0
        failed_p2_percentage = round((failed_p2_count / total_failed_challenges) * 100, 2) if total_failed_challenges else 0
        efficiency_ratio = round(winrate / average_duration_challenge, 2)

        metrics_dict = {
            "Total Number Challenges": total_challenges,
            "Total Passed Challenges": total_passed_challenges,
            "Total Failed Challenges": total_failed_challenges,
            "Winrate": winrate,
            "Average Duration Challenge": average_duration_challenge,
            "Average Duration Passed": average_duration_passed,
            "Average Duration Failed": average_duration_failed,
            "Max Consecutive Passed": max_cons_wins,
            "Max Consecutive Losses": max_cons_losses,
            "Average Consecutive Passed": average_cons_wins,
            "Average Consecutive Losses": average_cons_losses,
            "Failed Phase 1 Percentage": failed_p1_percentage,
            "Failed Phase 2 Percentage": failed_p2_percentage,
            "Efficiency Ratio": efficiency_ratio
        }

        return metrics_dict

    def _calculate_metrics_funded(self):
        df = self.df.copy()
        df["Outcome"] = df["Outcome"].astype(str).str.strip()
        df["Phase"] = pd.to_numeric(df["Phase"], errors = "coerce").fillna(0).astype(int)
        df["Duration"] = pd.to_numeric(df["Duration"], errors = "coerce").fillna(0)
        df["Start Balance"] = pd.to_numeric(df["Start Balance"], errors = "coerce").fillna(0)
        df["Ending Balance"] = pd.to_numeric(df["Ending Balance"], errors = "coerce").fillna(0)

        challenge_groups = df.groupby(["Challenge Number"])
        total_challenges = challenge_groups.ngroups
        total_passed_challenges = total_payouts = total_failed_challenges = 0
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
                total_passed_challenges += 1
                total_payouts += len(payouts)
                passed_durations.append(total_duration)
                challenge_outcomes.append("Payout")
                payout_profits.extend((payouts["Ending Balance"] - payouts["Start Balance"]).tolist())
            else:
                total_failed_challenges += 1
                failed_durations.append(total_duration)
                challenge_outcomes.append("Failed")

        challenge_winrate = round((total_passed_challenges / total_challenges) * 100, 2) if total_challenges else 0
        payout_winrate = round((total_payouts / (total_payouts + total_failed_challenges)) * 100, 2) if (total_payouts + total_failed_challenges) else 0
        average_duration_total = round(sum(challenge_durations) / len(challenge_durations), 2) if challenge_durations else 0
        average_duration_passed = round(sum(passed_durations) / len(passed_durations), 2) if passed_durations else 0
        average_duration_failed = round(sum(failed_durations) / len(failed_durations), 2) if failed_durations else 0

        if challenge_outcomes:
            series = pd.Series(challenge_outcomes)
            groups = (series != series.shift()).cumsum()
            streaks = series.groupby(groups).agg(['first', 'size'])
            win_streaks = streaks[streaks['first'] == 'Payout']["size"]
            loss_streaks = streaks[streaks['first'] == 'Failed']["size"]
            max_cons_wins = int(win_streaks.max()) if not win_streaks.empty else 0
            max_cons_losses = int(loss_streaks.max()) if not loss_streaks.empty else 0
            average_cons_wins = round(win_streaks.mean(), 2) if not win_streaks.empty else 0
            average_cons_losses = round(loss_streaks.mean(), 2) if not loss_streaks.empty else 0
        else:
            max_cons_wins = max_cons_losses = average_cons_losses = average_cons_wins = 0

        df_sorted = df.sort_values(["Challenge Number", "Phase"])
        all_payout_series = (df_sorted["Outcome"] == "Payout").astype(int)
        streak_groups = (all_payout_series != all_payout_series.shift()).cumsum()
        streaks = all_payout_series.groupby(streak_groups).sum()
        all_challenge_payout_streaks = streaks[streaks > 0].tolist()
        max_cons_payouts_per_challenge = max(all_challenge_payout_streaks) if all_challenge_payout_streaks else 0
        average_cons_payouts_per_challenge = round(sum(all_challenge_payout_streaks) / len(all_challenge_payout_streaks), 2) if all_challenge_payout_streaks else 0

        average_profit_per_payout = round(sum(payout_profits) / len(payout_profits), 2) if payout_profits else 0
        total_challenge_profits = []
        for _, group in df.groupby("Challenge Number"):
            payouts = group[group["Outcome"] == "Payout"]
            total_profit = (payouts["Ending Balance"] - payouts["Start Balance"]).sum() if not payouts.empty else -80
            total_challenge_profits.append(total_profit)
        average_total_profit_per_challenge = round(sum(total_challenge_profits) / len(total_challenge_profits), 2) if total_challenge_profits else 0

        df["End Phase Date"] = pd.to_datetime(df["End Phase Date"], errors = "coerce")
        df["PnL"] = np.where(
            df["Outcome"] == "Payout",
            df["Ending Balance"] - df["Start Balance"],
            np.where(df["Outcome"] == "Failed", -80, 0)
        )

        df["Month"] = df["End Phase Date"].dt.to_period("M").astype(str)
        monthly_pnl = df.groupby("Month")["PnL"].sum()
        winning_months = int((monthly_pnl > 0).sum())
        losing_months = int((monthly_pnl < 0).sum())
        monthly_winrate = round((winning_months / (winning_months + losing_months)) * 100, 2) if (winning_months + losing_months) else 0
        average_monthly_profit = round(monthly_pnl[monthly_pnl > 0].mean(), 2) if (monthly_pnl > 0).any() else 0
        average_monthly_loss = round(monthly_pnl[monthly_pnl < 0].mean(), 2) if (monthly_pnl < 0).any() else 0
        monthly_wl_ratio = round(winning_months / losing_months, 2) if losing_months > 0 else float('inf')
        profitability_ratio_payout = round(((payout_winrate / 100) * average_cons_payouts_per_challenge * average_profit_per_payout) / 80, 2)
        profitability_ratio_monthly = round(((monthly_winrate / 100) * average_monthly_profit) / (average_monthly_loss * -1), 2)
        challenge_efficiency_ratio = round(average_total_profit_per_challenge / total_failed_challenges, 2)
        overall_risk_adjusted_return = round(challenge_efficiency_ratio * profitability_ratio_monthly, 2)

        metrics_dict = {
            "Number Passed Challenges": total_passed_challenges,
            "Number Failed Challenges": total_failed_challenges,
            "Challenge Winrate": challenge_winrate,
            "Payout Winrate": payout_winrate,
            "Average Duration Total": average_duration_total,
            "Average Duration Passed": average_duration_passed,
            "Average Duration Failed": average_duration_failed,
            "Max Consecutive Passed Challenges": max_cons_wins,
            "Max Consecutive Failed Challenges": max_cons_losses,
            "Average Consecutive Passed Challenges": average_cons_wins,
            "Average Consecutive Failed Challenges": average_cons_losses,
            "Max Consecutive Payouts": max_cons_payouts_per_challenge,
            "Average Payouts Per Challenge": average_cons_payouts_per_challenge,
            "Average Profit Per Payout": average_profit_per_payout,
            "Average Profit Per Challenge": average_total_profit_per_challenge,
            "Winning Months": winning_months,
            "Losing Months": losing_months,
            "Monthly Winrate": monthly_winrate,
            "Average Monthly Profit": average_monthly_profit,
            "Average Monthly Loss": average_monthly_loss,
            "Monthly W/L Ratio": monthly_wl_ratio,
            "Challenge Efficiency": challenge_efficiency_ratio,
            "Overall Risk Adjusted Returns": overall_risk_adjusted_return,
            "Profitability Ratio Payout": profitability_ratio_payout,
            "Profitability Ratio Monthly": profitability_ratio_monthly
        }

        return metrics_dict

    def _calculate_consecutive_metrics(self, series, outcome):
        mask = series == outcome
        streaks = mask.groupby((mask != mask.shift()).cumsum()).sum()
        streaks = streaks[streaks > 0]
        return streaks