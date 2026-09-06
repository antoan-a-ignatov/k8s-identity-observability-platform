import os

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, session, url_for

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

# oidc client setup
oauth = OAuth(app)
oauth.register(
    name="keycloak",
    client_id=os.environ["KEYCLOAK_CLIENT_ID"],
    client_secret=os.environ["KEYCLOAK_CLIENT_SECRET"],
    server_metadata_url=(
        f'{os.environ["KEYCLOAK_SERVER_URL"]}/realms/'
        f'{os.environ["KEYCLOAK_REALM"]}/.well-known/openid-configuration'
    ),
    client_kwargs={"scope": "openid profile email"},
)


@app.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", user=user)


@app.route("/login")
def login():
    return oauth.keycloak.authorize_redirect(os.environ["REDIRECT_URI"])


@app.route("/callback")
def callback():
    token = oauth.keycloak.authorize_access_token()
    session["user"] = token.get("userinfo")
    return redirect(url_for("protected"))


@app.route("/protected")
def protected():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return render_template("protected.html", user=user)


@app.route("/logout")
def logout():
    session.pop("user", None)
    base_url = os.environ["REDIRECT_URI"].rsplit("/callback", 1)[0]
    logout_url = (
        f'{os.environ["KEYCLOAK_BROWSER_URL"]}/realms/'
        f'{os.environ["KEYCLOAK_REALM"]}/protocol/openid-connect/logout'
        f'?redirect_uri={base_url}'
    )
    return redirect(logout_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
