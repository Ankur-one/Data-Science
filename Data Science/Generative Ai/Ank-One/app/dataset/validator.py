class DatasetValidator:

    @staticmethod
    def validate(df):

        print("=" * 60)
        print("Dataset Validation")
        print("=" * 60)

        print(f"Rows : {len(df)}")
        print(f"Columns : {len(df.columns)}")

        print("\nColumn Names")
        print(df.columns.tolist())

        print("\nMissing Values")
        print(df.isnull().sum())

        print("\nDuplicate Rows")
        print(df.duplicated().sum())

        print("\nFirst Five Rows")

        print(df.head())