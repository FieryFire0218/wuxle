from flask import Flask, render_template, request, jsonify
from datetime import datetime, UTC

from sqlalchemy import select

from database import SessionLocal
from models import Novel
from compare import (
    compare_guess,
    _normalize_rating_5,
    _round_to_half
)

app = Flask(__name__)

def get_novels():
    with SessionLocal() as session:
        novels = session.scalars(
            select(Novel).order_by(Novel.id)
        ).all()

        return [novel.to_dict() for novel in novels]

def get_daily_answer(novels):
    if not novels:
        return None

    idx = (
        datetime.now(UTC).date().toordinal()
        % len(novels)
    )

    return novels[idx]

@app.route("/")
def index():
    novels = get_novels()

    return render_template(
        "index.html",
        novels=[novel["title"] for novel in novels]
    )

@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request"}), 400

    guess_title = data.get("title")

    if not isinstance(guess_title, str):
        return jsonify({"error": "Invalid title"}), 400

    novels = get_novels()

    guess_novel = next(
        (
            novel for novel in novels
            if novel["title"].lower() == guess_title.lower()
        ),
        None
    )

    if not guess_novel:
        return jsonify({"error": "Novel not found"}), 400

    answer = get_daily_answer(novels)

    if not answer:
        return jsonify({
            "error": "No novels available"
        }), 503

    feedback = compare_guess(guess_novel, answer)

    return jsonify(feedback)

@app.route("/answer")
def get_answer():
    novels = get_novels()

    answer = get_daily_answer(novels)

    if not answer:
        return jsonify({
            "error": "No novels available"
        }), 503

    # normalize rating to 0-5 for the UI
    r_raw = _normalize_rating_5(
        answer.get("rating")
    )

    r5 = None

    if r_raw is not None:
        r5 = max(
            0.0,
            min(5.0, _round_to_half(r_raw))
        )

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
