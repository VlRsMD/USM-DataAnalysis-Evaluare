from io_utils import get_paths, load_data
from descriptive import descriptive_analysis
from diagnostic import diagnostic_analysis
from predictive import predictive_analysis
from prescriptive import prescriptive_analysis


def main() -> None:
    input_path, output_dir = get_paths()
    print(f"Citind datele din: {input_path}")
    df = load_data(input_path)

    print("1) Analiză descriptivă...")
    descriptive_analysis(df, output_dir)

    print("2) Analiză diagnostică...")
    diagnostic_analysis(df, output_dir)

    print("3) Analiză predictivă (scor de risc)...")
    df_with_risk = predictive_analysis(df, output_dir)

    print("4) Analiză prescriptivă (selecția clienților pentru retenție)...")
    prescriptive_analysis(df_with_risk, output_dir)

    print(f"Analize terminate. CSV-urile sunt în: {output_dir}")


if __name__ == "__main__":
    main()
