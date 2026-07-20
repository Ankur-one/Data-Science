def sentence_length(df):
    """Compute sentence length statistics and return the dataframe with length columns."""
    print("\nCleaning missing values before analysis...")

    # Remove rows where English or Hindi is missing
    df = df.dropna(subset=["english", "hindi"]).copy()

    # Convert to string
    df["english"] = df["english"].astype(str)
    df["hindi"] = df["hindi"].astype(str)

    # Calculate sentence length
    df["english_length"] = df["english"].str.len()
    df["hindi_length"] = df["hindi"].str.len()

    print("\nEnglish Sentence Length Statistics")
    print(df["english_length"].describe())

    print("\nHindi Sentence Length Statistics")
    print(df["hindi_length"].describe())

    return df


def plot_sentence_length(df, bins: int = 50, save_path: str | None = None):
    """Plot histograms of sentence lengths for English and Hindi.

    If matplotlib is not available, prints a short summary instead.
    Returns path to saved figure when `save_path` is provided.
    """
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib not available — skipping plots. Install matplotlib to enable plotting.")
        return None

    # ensure length columns exist
    if "english_length" not in df.columns or "hindi_length" not in df.columns:
        df = sentence_length(df)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].hist(df["english_length"].dropna(), bins=bins, color="C0")
    axes[0].set_title("English sentence length")
    axes[0].set_xlabel("characters")

    axes[1].hist(df["hindi_length"].dropna(), bins=bins, color="C1")
    axes[1].set_title("Hindi sentence length")
    axes[1].set_xlabel("characters")

    plt.tight_layout()

    if save_path:
        from pathlib import Path

        p = Path(save_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(p)
        print(f"Saved plot to {p}")
        plt.close(fig)
        return str(p)

    plt.show()
    return None