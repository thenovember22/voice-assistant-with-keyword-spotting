from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import re

from flask_cors import CORS
from flask import Flask, jsonify, request

sys.path.append(str(Path(__file__).resolve().parents[1]))

import calculator
import musicLibrary


app = Flask(__name__)
CORS(app)


def generate_response(message: str) -> dict:
    normalized = message.lower()

    if "goodbye" in normalized or normalized == "bye":
        return {"reply": "Goodbye Bhargav, shutting down."}
    if re.search(r"\btime\b", normalized):
        ist = timezone(timedelta(hours=5, minutes=30))
        current_time = datetime.now(ist).strftime("%I:%M %p")
        return {"reply": f"The time is {current_time}."}
    if normalized.startswith("play"):
        song = normalized.replace("play", "", 1).strip()
        link = musicLibrary.music.get(song)
        if link:
            return {
                "reply": f"Playing {song}.",
                "action": {"type": "open_url", "url": link},
            }
        return {"reply": "I cannot find that song in your library."}
    if "calculate" in normalized or "what is" in normalized:
        return {"reply": calculator.calculate(message)}
    if any(greeting in normalized for greeting in ("hello", "hi", "hey")):
        return {"reply": "Hello Bhargav. Lilly is online and listening."}
    if "who are you" in normalized:
        return {
            "reply": "I'm Lilly, your AI voice assistant interface. Sharp edges, green glow, and useful answers."
        }
    if "thank" in normalized:
        return {"reply": "You're welcome. Keep going."}

    return {
        "reply": (
            "I heard you. Right now I can answer time, calculator, music, and goodbye commands. "
            "We can add more of your desktop assistant commands next."
        )
    }


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Message is required."}), 400

    return jsonify(generate_response(message))


if __name__ == "__main__":
    app.run(debug=True)
