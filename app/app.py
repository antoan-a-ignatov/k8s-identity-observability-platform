from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def health():
    return jsonify(status="ok")


@app.route("/protected")
def protected():
    # Keycloak token validation added in the Identity / App Integration milestones
    return jsonify(message="protected route placeholder")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
