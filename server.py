# server.py
from flask import Flask, jsonify, request, render_template
import os
import json

app = Flask(__name__, static_folder="public", static_url_path="")

GAMES_DIR = "games"
os.makedirs(GAMES_DIR, exist_ok=True)

def game_path(game_id):
    return os.path.join(GAMES_DIR, f"{game_id}.json")

@app.get("/game/<game_id>")
def get_game(game_id):
    path = game_path(game_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Game not found"}), 404

@app.post("/game/<game_id>")
def save_game(game_id):
    data = request.json
    path = game_path(game_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return "OK"

@app.get("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run("0.0.0.0", 3000, debug=True)