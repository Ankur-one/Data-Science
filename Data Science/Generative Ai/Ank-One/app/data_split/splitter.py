"""
=========================================
Ank-One
Dataset Splitter
=========================================
"""

from pathlib import Path

from sklearn.model_selection import train_test_split


class DatasetSplitter:

    def split(self, df):

        print("=" * 60)
        print("Splitting Dataset")
        print("=" * 60)

        # Train = 80%
        train_df, temp_df = train_test_split(
            df,
            test_size=0.20,
            random_state=42,
            shuffle=True
        )

        # Validation = 10%
        # Test = 10%
        validation_df, test_df = train_test_split(
            temp_df,
            test_size=0.50,
            random_state=42,
            shuffle=True
        )

        print(f"Train      : {len(train_df)}")
        print(f"Validation : {len(validation_df)}")
        print(f"Test       : {len(test_df)}")

        return train_df, validation_df, test_df

    def save(self, train_df, validation_df, test_df):

        Path("data/train").mkdir(parents=True, exist_ok=True)
        Path("data/validation").mkdir(parents=True, exist_ok=True)
        Path("data/test").mkdir(parents=True, exist_ok=True)

        train_df.to_csv(
            "data/train/train.csv",
            index=False,
            encoding="utf-8"
        )

        validation_df.to_csv(
            "data/validation/validation.csv",
            index=False,
            encoding="utf-8"
        )

        test_df.to_csv(
            "data/test/test.csv",
            index=False,
            encoding="utf-8"
        )

        print("\nDatasets Saved Successfully")