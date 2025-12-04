from pathlib import Path
import pandas as pd


def diagnostic_analysis(df: pd.DataFrame, output_dir: Path) -> None:
    means_by_churn = (
        df.groupby("Churn")[
            ["SatisfactionScore", "NumTicketsLast6M", "LatePaymentsLast6M"]
        ]
        .mean()
        .reset_index()
    )
    means_by_churn.to_csv(output_dir / "means_by_churn.csv", index=False)

    churn_by_plan = (
        df.groupby("PlanType")["Churn"]
        .agg(churn_rate="mean", n="count")
        .reset_index()
    )
    churn_by_plan.to_csv(output_dir / "diagnostic_churn_by_plantype.csv", index=False)

    def satisfaction_band(score: float) -> str:
        if score <= 4:
            return "1-4"
        elif score <= 7:
            return "5-7"
        else:
            return "8-10"

    df["SatisfactionBand"] = df["SatisfactionScore"].apply(satisfaction_band)

    churn_by_band = (
        df.groupby("SatisfactionBand")["Churn"]
        .agg(churn_rate="mean", n="count")
        .reset_index()
    )
    band_order = pd.Categorical(
        churn_by_band["SatisfactionBand"],
        categories=["1-4", "5-7", "8-10"],
        ordered=True,
    )
    churn_by_band = churn_by_band.sort_values("SatisfactionBand", key=lambda s: band_order)
    churn_by_band.to_csv(output_dir / "churn_by_satisfaction_band.csv", index=False)

    corr_df = (
        df[["SatisfactionScore", "TenureMonths", "NumTicketsLast6M", "Churn"]]
        .corr()
        ["Churn"]
        .drop("Churn")
        .reset_index()
        .rename(columns={"index": "variable", "Churn": "correlation_with_churn"})
    )
    corr_df.to_csv(output_dir / "correlations_with_churn.csv", index=False)
