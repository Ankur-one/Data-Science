from flask import Flask, render_template, request, send_file
from google.cloud import texttospeech
import json
import os
import tempfile

app = Flask(__name__)

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", CREDENTIALS_FILE)

init_error = None
client = None

try:
    if not os.path.isfile(CREDENTIALS_FILE):
        raise FileNotFoundError(f"Google credentials file not found: {CREDENTIALS_FILE}")
    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        credentials_data = json.load(f)
        if not isinstance(credentials_data, dict) or not credentials_data:
            raise ValueError("Google credentials file is empty or invalid JSON.")
    client = texttospeech.TextToSpeechClient()
except Exception as exc:
    init_error = str(exc)


@app.route("/")
def index():
    return render_template("index.html", error=init_error)


@app.route("/convert", methods=["POST"])
def convert():
    if init_error:
        return render_template("index.html", error=init_error)

    text = request.form["text"]
    voice_name = request.form["voice"]
    filename = request.form["filename"]

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    temp.write(response.audio_content)
    temp.close()

    return send_file(
        temp.name,
        as_attachment=True,
        download_name=f"{filename}.mp3",
        mimetype="audio/mpeg"
    )


if __name__ == "__main__":
    app.run(debug=True)