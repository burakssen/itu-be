from flask import Flask
from flask_wtf.csrf import CSRFProtect
import view
import os

from flask_login import LoginManager
from entities.Entities import DataBase

lm = LoginManager()

csrf = CSRFProtect()


def create_app():
    global lm
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
    app.add_url_rule("/classes/<string:classCode>/<string:videoCode>",view_func=view.video_page,methods=["GET","POST"])
    app.add_url_rule("/adminpanel/",view_func=view.admin_panel_page, methods=["GET","POST"])
    app.add_url_rule("/adminpanel/users/",view_func=view.admin_users_page, methods=["GET","POST"])
    app.add_url_rule("/logout",view_func=view.log_out, methods=["GET","POST"])

    lm.init_app(app)
    lm.login_view = "auth_page"

    db = DataBase("Itu-be","burakssen", "18Kalemlik09.")
    app.config["db"] = db

    csrf.init_app(app)
    return app

@lm.user_loader
def load_user(username):
    db = app.config['db']
    return db.get_user(username)
   
app = create_app()
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0',port=port,debug=True)