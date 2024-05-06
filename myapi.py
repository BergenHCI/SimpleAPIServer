from flask import Flask

app = Flask(__name__)


@app.route("/me")
def me_api():
    user = {"name": "UserName", "age": 99}
    return user



