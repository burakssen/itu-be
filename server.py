from flask import Flask, request
import view
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config.from_object('settings')
    app.add_url_rule("/",view_func=view.auth_page,methods=["GET", "POST"])
    app.add_url_rule("/<string:info>",view_func=view.auth_page,methods=["GET", "POST"])
    app.add_url_rule("/SignUp",view_func=view.account_create_page,methods=["GET", "POST"])
    app.add_url_rule("/profile",view_func=view.profile_page,methods=["GET", "POST"])
    
    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port,debug=True)