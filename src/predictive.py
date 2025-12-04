from pathlib import Path
import numpy as np
import pandas as pd


def predictive_analysis(df: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    risk_score = np.zeros(len(df), dtype=int)

    risk_score += np.where(df["SatisfactionScore"] < 6, 2, 0)
    risk_score += np.where(df["NumTicketsLast6M"] > 3, 2, 0)
    risk_score += np.where(df["LatePaymentsLast6M"] >= 2, 1, 0)
    risk_score += np.where(df["TenureMonths"] < 12, 1, 0)
    risk_score += np.where(df["Autopay"] == 0, 1, 0)

    df["RiskScore"] = risk_score

    conditions = [
        df["RiskScore"] <= 2,
        df["RiskScore"].between(3, 4),
        df["RiskScore"] >= 5,
    ]
    choices = ["Low risk", "Medium risk", "High risk"]
    df["RiskCategory"] = np.select(conditions, choices, default="Low risk")

    df["RiskCategory"] = pd.Categorical(
        df["RiskCategory"],
        categories=["Low risk", "Medium risk", "High risk"],
        ordered=True,
    )

    risk_summary = (
        df.groupby("RiskCategory")
        .agg(
            num_clients=("CustomerID", "count"),
            churn_rate=("Churn", "mean"),
        )
        .reset_index()
    )
    risk_summary.to_csv(output_dir / "risk_category_churn_summary.csv", index=False)

    df.to_csv(output_dir / "clients_with_risk_scores.csv", index=False)

    return df
