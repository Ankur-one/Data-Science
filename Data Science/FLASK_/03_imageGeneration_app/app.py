import base64
import os
from pathlib import Path
from urllib.request import urlopen

from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

# Create static folder if it doesn't exist
os.makedirs("static", exist_ok=True)


def get_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip().upper() == "OPENAI_API_KEY":
                return value.strip().strip('"').strip("'")

    return None


def generate_image(prompt):
    api_key = get_openai_api_key()
    if not api_key:
        error_message = "OpenAI API key is not configured. Set OPENAI_API_KEY or add it to .env."
        app.logger.error(error_message)
        return None, error_message

    client = OpenAI(api_key=api_key)

    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            quality="high"
        )

        image_item = response.data[0]
        image_path = "static/generated_image.png"

        if getattr(image_item, "b64_json", None):
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(image_item.b64_json))
        else:
            image_url = getattr(image_item, "url", None)
            if not image_url and isinstance(image_item, dict):
                image_url = image_item.get("url")
            if not image_url:
                return None, "The API did not return an image payload."

            with urlopen(image_url) as image_response, open(image_path, "wb") as f:
                f.write(image_response.read())

        return image_path, None

    except Exception as exc:
        app.logger.exception("Image generation failed")
        return None, f"Image generation failed: {exc}"


@app.route("/", methods=["GET", "POST"])
def index():
    image_path = None
    error = None

    if request.method == "POST":
        prompt = request.form.get("prompt")

        if prompt:
            image_path, error = generate_image(prompt)

            if image_path is None:
                error = error or "Failed to generate image."

        else:
            error = "Please enter a prompt."

    return render_template(
        "index.html",
        image_path=image_path,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)