"""
===========================================
Ank-One
Dataset Loader
===========================================
"""

from pathlib import Path
import pandas as pd


class DatasetLoader:

    def __init__(self):

        self.dataset_path = Path(
            "data/raw/english_hindi.csv"
        )

    def load_dataset(self):

        df = pd.read_csv(self.dataset_path)

        return df


if __name__ == "__main__":

    loader = DatasetLoader()

    df = loader.load_dataset()

    print(df.head())