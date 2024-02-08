from flask import Flask

from api.routes.user import user
from api.routes.post import post


def run_api():
    app = Flask(__name__)
    app.register_blueprint(user, url_prefix='/api/user')
    app.register_blueprint(post, url_prefix='/api/post')
    app.run(debug=False)
