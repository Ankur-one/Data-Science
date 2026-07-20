from .config import SAVE_PATH


class DatasetExporter:

    @staticmethod
    def save(df):

        SAVE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_csv(
            SAVE_PATH,
            index=False,
            encoding="utf-8"
        )

        print("=" * 60)
        print("Dataset Saved Successfully")
        print("=" * 60)

        print(SAVE_PATH)