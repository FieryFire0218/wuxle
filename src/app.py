from flask import Flask, render_template, request, jsonify
import json, random, datetime
from compare import compare_guess
import datetime

app = Flask(__name__)

# Load data
with open("data/novels.json", "r", encoding="utf-8") as f:
    novels = json.load(f)

# Pick daily novel deterministically
today = datetime.datetime.now(datetime.UTC).date().toordinal()
answer = novels[today % len(novels)]

@app.route("/")
def index():
    return render_template("index.html", novels=[n["title"] for n in novels])

@app.route("/guess", methods=["POST"])
def guess():
    guess_title = request.json["title"]
    guess_novel = next((n for n in novels if n["title"].lower() == guess_title.lower()), None)
    if not guess_novel:
        return jsonify({"error": "Novel not found"}), 400

    feedback = compare_guess(guess_novel, answer)
    return jsonify(feedback)

@app.route("/answer")
def get_answer():
    return jsonify({
        "title": answer["title"],
        "author": answer["author"],
        "translator": answer["translator"],
        "genres": answer["genres"],
        "rating": answer["rating"],
        "chapters": answer["chapters"]
    })


if __name__ == "__main__":
    app.run(debug=True)
