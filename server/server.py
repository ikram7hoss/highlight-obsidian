from flask import Flask, request, jsonify
from flask_cors import CORS

from notes import add_highlight

app = Flask(__name__)
CORS(app)  # autorise l'extension du navigateur à appeler le serveur


@app.post("/highlight")
def highlight():
    data = request.get_json(silent=True) or {}

    # vérifier que les 4 champs sont présents
    missing = [k for k in ("color", "text", "url", "title") if k not in data]
    if missing:
        return jsonify(error=f"Missing fields: {missing}"), 400

    try:
        add_highlight(data["color"], data["text"], data["url"], data["title"])
    except ValueError as e:  # couleur inconnue
        return jsonify(error=str(e)), 400

    return jsonify(status="ok")


if __name__ == "__main__":
    # 127.0.0.1 = accessible uniquement depuis ton ordinateur
    app.run(host="127.0.0.1", port=5000)