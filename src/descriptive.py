from pathlib import Path
import pandas as pd


def descriptive_analysis(df: pd.DataFrame, output_dir: Path) -> None:
    numeric_cols = ["MonthlyRevenue", "Age", "TenureMonths", "SatisfactionScore"]
    desc = df[numeric_cols].agg(["mean", "median", "min", "max", "std"]).reset_index()
    desc = desc.rename(columns={"index": "stat"})
    desc.to_csv(output_dir / "descriptive_numeric_stats.csv", index=False)

    for col in ["PlanType", "Segment", "Region"]:
        freq = (
            df[col]
            .value_counts(dropna=False)
            .rename_axis(col)
            .reset_index(name="count")
        )
        freq["percent"] = freq["count"] / freq["count"].sum()
        freq.to_csv(output_dir / f"frequency_{col.lower()}.csv", index=False)

    global_churn_rate = df["Churn"].mean()
    churn_global_df = pd.DataFrame(
        {"metric": ["global_churn_rate"], "value": [global_churn_rate]}
    )
    churn_global_df.to_csv(output_dir / "churn_global_rate.csv", index=False)

    for col in ["PlanType", "Region", "Segment"]:
        churn_by = (
            df.groupby(col)["Churn"]
            .agg(churn_rate="mean", n="count")
            .reset_index()
        )
        churn_by.to_csv(output_dir / f"churn_by_{col.lower()}.csv", index=False)
