import pandas as pd
from pathlib import Path


def get_paths() -> tuple[Path, Path]:
    src_dir = Path(__file__).resolve().parent
    project_root = src_dir.parent
    dataset_dir = project_root / "dataset"
    input_path = dataset_dir / "Customer_analytics.xlsx"
    output_dir = dataset_dir / "outputs"

    output_dir.mkdir(parents=True, exist_ok=True)

    return input_path, output_dir


def load_data(input_path: Path) -> pd.DataFrame:
    df = pd.read_excel(input_path, sheet_name="Clienti")
    return df
