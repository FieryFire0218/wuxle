from flask import Flask, render_template, request, jsonify
import json
from pathlib import Path
from datetime import datetime, UTC
from compare import compare_guess, _normalize_rating_5, _round_to_half

app = Flask(__name__)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "novels.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    novels = json.load(f)

def get_daily_answer(novels):
    if not novels:
        return None
    idx = datetime.now(UTC).date().toordinal() % len(novels)
    return novels[idx]

@app.route("/")
def index():
    return render_template("index.html", novels=[n["title"] for n in novels])

@app.route("/guess", methods=["POST"])
def guess():
    guess_title = request.json["title"]
    guess_novel = next((n for n in novels if n["title"].lower() == guess_title.lower()), None)
    if not guess_novel:
        return jsonify({"error": "Novel not found"}), 400

    answer = get_daily_answer(novels)
    if not answer:
        return jsonify({"error": "No novels available"}), 503
    
    feedback = compare_guess(guess_novel, answer)
    return jsonify(feedback)

@app.route("/answer")
def get_answer():
    answer = get_daily_answer(novels)
    if not answer:
        return jsonify({"error": "No novels available"}), 503
    # Normalize rating to 0–5 for UI
    r_raw = _normalize_rating_5(answer.get("rating"))
    r5 = None
    if r_raw is not None:
        r5 = max(0.0, min(5.0, _round_to_half(r_raw)))
    return jsonify({
        "title": answer["title"],
        "author": answer["author"],
        "translator": answer["translator"],
        "genres": answer["genres"],
        "rating": answer["rating"],
        "rating5": r5,
        "chapters": answer["chapters"]
    })


if __name__ == "__main__":
    app.run(debug=True)
