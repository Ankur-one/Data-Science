import base64
from io import BytesIO

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template

app = Flask(__name__)


def fig_to_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    plt.close(fig)
    return encoded


def build_plots(iris):
    sns.set_theme(style="whitegrid")

    scatter_fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=iris, x="sepal_length", y="sepal_width", hue="species", s=70, ax=ax)
    ax.set_title("Sepal Length vs Sepal Width")
    ax.set_xlabel("Sepal Length")
    ax.set_ylabel("Sepal Width")
    scatter_plot = fig_to_base64(scatter_fig)

    hist_fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(data=iris, x="petal_length", hue="species", kde=True, ax=ax)
    ax.set_title("Petal Length Distribution")
    ax.set_xlabel("Petal Length")
    ax.set_ylabel("Count")
    hist_plot = fig_to_base64(hist_fig)

    corr_fig, ax = plt.subplots(figsize=(6, 4))
    numeric = iris.select_dtypes(include=["float64", "int64"])
    sns.heatmap(numeric.corr(method="pearson"), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Correlation Heatmap")
    corr_plot = fig_to_base64(corr_fig)

    return {"scatter": scatter_plot, "histogram": hist_plot, "heatmap": corr_plot}


@app.route("/")
def home():
    iris = sns.load_dataset("iris")
    preview = iris.head(8).to_html(index=False)
    summary = iris.describe().round(2).to_html()
    species_counts = iris["species"].value_counts().to_dict()
    plots = build_plots(iris)

    return render_template(
        "index.html",
        title="Iris Dataset EDA",
        preview=preview,
        summary=summary,
        species_counts=species_counts,
        plots=plots,
        rows=iris.shape[0],
        columns=iris.shape[1],
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")