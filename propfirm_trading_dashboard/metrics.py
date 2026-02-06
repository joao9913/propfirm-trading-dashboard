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

        print(f"Total Challenges: {total_challenges}")
        print(f"Total Won Challenges: {total_passed_challenges}")
        print(f"Total Failed Challenges: {total_failed_challenges}")
        print(f"Winrate: {winrate}")
        print(f"Average Duration Challenge: {average_duration_challenge}")
        print(f"Average Duration Passed Challenges: {average_duration_passed}")
        print(f"Average Duration Failed Challenges: {average_duration_failed}")
        print(f"Max Consecutive Passed Challenges: {max_cons_wins}")
        print(f"Max Consecutive Failed Challenges: {max_cons_losses}")
        print(f"Average Consecutive Passed Challenges: {average_cons_wins}")
        print(f"Average Consecutive Failed Challenges: {average_cons_losses}")
        print(f"Failed P1 Percentage: {failed_p1_percentage}")
        print(f"Failed P2 Percentage: {failed_p2_percentage}")
        print(f"Efficiency Ratio: {efficiency_ratio}")

    def _calculate_metrics_funded(self):
        print("Calculating Funded")

    def _calculate_consecutive_metrics(self, series, outcome):
        mask = series == outcome
        streaks = mask.groupby((mask != mask.shift()).cumsum()).sum()
        streaks = streaks[streaks > 0]
        return streaks