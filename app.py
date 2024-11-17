from config import config
from flask import Flask


# Wants to move routing before app init, which leads to error
# autopep8: off
app = Flask(__name__)

import routing
# autopep8: on

# Security
app.secret_key = config["security"]["session_secret"]
app.jinja_options["autoescape"] = True

# General
app.config['MAX_CONTENT_LENGTH'] = int(config["general"]["upload_limit"])
app.debug = config["general"]["debug"] == "true"


if __name__ == "__main__":
    app.run(host=config["general"]["host"])
