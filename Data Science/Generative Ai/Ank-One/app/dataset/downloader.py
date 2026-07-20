from datasets import load_dataset

from .config import DATASET_NAME, LANGUAGE_PAIR


class DatasetDownloader:

    def download(self):
        print("Downloading dataset...")

        dataset = load_dataset(
            DATASET_NAME,
            LANGUAGE_PAIR
        )

        return dataset

    def convert_to_dataframe(self, dataset):
        train_df = dataset["train"].to_pandas()
        return train_df

    def extract_translation(self, df):

        df["english"] = df["translation"].apply(
            lambda x: x["en"]
        )

        df["hindi"] = df["translation"].apply(
            lambda x: x["hi"]
        )

        df = df[["english", "hindi"]]

        return df