from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
import view
import os

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config.from_object('settings')
    app.add_url_rule("/",view_func=view.auth_page,methods=["GET", "POST"])
    app.add_url_rule("/<string:info>",view_func=view.auth_page,methods=["GET", "POST"])
    app.add_url_rule("/SignUp",view_func=view.account_create_page,methods=["GET", "POST"])
    app.add_url_rule("/profile/<string:user>",view_func=view.profile_page,methods=["GET", "POST"])
    app.add_url_rule("/profile/<string:user>/uploadvideo/",view_func=view.upload_video_page,methods=["GET","POST"])
    app.add_url_rule("/classes/",view_func=view.classes_page,methods=["GET","POST"])
    app.add_url_rule("/classes/<string:classCode>",view_func=view.class_page,methods=["GET","POST"])
    csrf.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port,debug=True)