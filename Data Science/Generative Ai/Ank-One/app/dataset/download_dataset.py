from app.dataset.downloader import DatasetDownloader
from app.dataset.config import SAVE_PATH


def main():
    downloader = DatasetDownloader()
    dataset = downloader.download()

    print(dataset)

    df = downloader.convert_to_dataframe(dataset)
    df = downloader.extract_translation(df)

    # ensure save directory exists
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SAVE_PATH, index=False)
    print(f"Saved {len(df)} rows to {SAVE_PATH}")

    return df


if __name__ == "__main__":
    main()