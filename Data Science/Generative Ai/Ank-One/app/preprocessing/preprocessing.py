"""
==========================================
Ank-One
Data Preprocessing Module
==========================================
"""


class DataPreprocessor:

    def clean(self, df):

        print("=" * 60)
        print("Cleaning Dataset")
        print("=" * 60)

        # Remove missing values
        df = df.dropna()

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Remove extra spaces
        df["english"] = df["english"].str.strip()
        df["hindi"] = df["hindi"].str.strip()

        print("Cleaning Completed")

        return df