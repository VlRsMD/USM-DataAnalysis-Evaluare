from pathlib import Path
import pandas as pd


def prescriptive_analysis(df: pd.DataFrame, output_dir: Path) -> None:
    """
    Lucrăm doar cu High risk.
    Presupunem o probabilitate fixă de păstrare de 70% pentru toți cei care primesc ofertă.
    NetValueIfOffer = 0.7 * ExpectedMarginNext6M – RetentionOfferCost
    Apoi selectăm clienți în limita unui buget total de 3000 EUR.
    """
    budget = 3000.0
    prob_keep_if_offer = 0.7

    high_risk = df[df["RiskCategory"] == "High risk"].copy()

    if high_risk.empty:
        print("Nu există clienți în categoria High risk.")
        return

    high_risk["RetentionProbIfOffer"] = prob_keep_if_offer
    high_risk["NetValueIfOffer"] = (
        high_risk["RetentionProbIfOffer"] * high_risk["ExpectedMarginNext6M"]
        - high_risk["RetentionOfferCost"]
    )

    high_risk_sorted = high_risk.sort_values("NetValueIfOffer", ascending=False)

    selected_rows = []
    total_cost = 0.0

    for _, row in high_risk_sorted.iterrows():
        cost = float(row["RetentionOfferCost"])
        net_val = float(row["NetValueIfOffer"])

        if net_val <= 0:
            continue

        if total_cost + cost <= budget:
            selected_rows.append(row)
            total_cost += cost

    if not selected_rows:
        print("Niciun client High risk nu are NetValueIfOffer pozitiv în limita bugetului.")
        return

    selected_df = pd.DataFrame(selected_rows)

    total_margin_recovered = (
        selected_df["RetentionProbIfOffer"] * selected_df["ExpectedMarginNext6M"]
    ).sum()
    total_net_value = selected_df["NetValueIfOffer"].sum()

    selected_cols = [
        "CustomerID",
        "RiskScore",
        "RiskCategory",
        "RetentionOfferCost",
        "ExpectedMarginNext6M",
        "RetentionProbIfOffer",
        "NetValueIfOffer",
        "PlanType",
        "Segment",
        "Region",
        "Churn",
    ]
    selected_cols = [c for c in selected_cols if c in selected_df.columns]

    selected_df[selected_cols].to_csv(
        output_dir / "selected_retention_clients.csv",
        index=False,
    )

    summary_df = pd.DataFrame(
        {
            "num_selected_clients": [len(selected_df)],
            "total_cost": [total_cost],
            "total_expected_margin_recovered": [total_margin_recovered],
            "total_net_value": [total_net_value],
            "budget": [budget],
        }
    )
    summary_df.to_csv(output_dir / "selected_retention_summary.csv", index=False)
