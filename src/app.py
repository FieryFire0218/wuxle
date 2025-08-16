from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Load JSON data once at startup
with open('data/novels.json', 'r', encoding='utf-8') as f:
    novels = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', novels=novels)

@app.route('/api/novels')
def api_novels():
    return jsonify(novels)

if __name__ == '__main__':
    app.run(debug=True)
