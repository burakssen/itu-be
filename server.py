from flask import Flask
from flask_wtf.csrf import CSRFProtect
import view
import os

from flask_login import LoginManager
from entities.DataBase import DataBase

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
    app.add_url_rule("/profile/<string:user>/uploadvideo/<string:info>/",view_func=view.upload_video_page,methods=["GET","POST"])
    app.add_url_rule("/classes/",view_func=view.all_classes_page,methods=["GET","POST"])
    app.add_url_rule("/classes/delete/<string:class_code>/",view_func=view.delete_class, methods=["GET","POST"])
    app.add_url_rule("/classes/<string:class_code>/",view_func=view.class_page,methods=["GET", "POST"])
    app.add_url_rule("/classes/<string:class_code>/video/<string:video_code>/", view_func=view.video_page, methods=["GET", "POST"])
    app.add_url_rule("/adminpanel/", view_func=view.admin_panel_page, methods=["GET", "POST"])
    app.add_url_rule("/adminpanel/users/", view_func=view.admin_users_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=view.log_out, methods=["GET", "POST"])
    app.add_url_rule("/adminpanel/users/delete/<int:user_id>", view_func=view.user_delete, methods=["GET", "POST"])
    app.add_url_rule("/adminpanel/users/activate/<int:user_id>", view_func=view.user_activate, methods=["GET", "POST"])
    app.add_url_rule("/classcreate/",view_func=view.create_class_page, methods=["GET", "POST"])
    app.add_url_rule("/classcreate/<string:info>/", view_func=view.create_class_page, methods=["GET", "POST"])
    app.add_url_rule("/access_denied/", view_func=view.access_denied, methods=["GET", "POST"])
    app.add_url_rule("/profile/<string:user>/classes/",view_func=view.personal_classes_page,methods=["GET","POST"])
    app.add_url_rule("/adminpanel/departments",view_func=view.department_page, methods=["GET","POST"])
    app.add_url_rule("/adminpanel/departments/delete/<string:department_code>", view_func=view.department_delete, methods=["GET","POST"])
    app.add_url_rule("/classes/<string:class_code>/addstudent/",view_func=view.student_add_page, methods=["GET","POST"])
    app.add_url_rule("/classes/<string:class_code>/deletestudent/<string:student_id>/",view_func=view.delete_student_from_class, methods=["GET","POST"])
    app.add_url_rule("/tutors/", view_func=view.tutor_list, methods=["GET", "POST"])
    app.add_url_rule("/classes/<string:class_code>/deletevideo/<string:video_code>/",view_func=view.delete_video,methods=["GET","POST"])
    app.add_url_rule("/classes/<string:class_code>/updateclass/",view_func=view.update_class_page,methods=["GET","POST"])
    app.add_url_rule("/classes/<string:class_code>/video/<string:video_code>/update", view_func=view.update_video_page,methods=["GET","POST"])
    app.add_url_rule("/profile/<string:user>/comments/",view_func=view.student_comments_page,methods=["GET","POST"])
    lm.init_app(app)
    lm.login_view = "auth_page"
    
    db = DataBase()
    app.config["db"] = db
    app.jinja_env.filters['zip'] = zip

    csrf.init_app(app)
    return app


@lm.user_loader
def load_user(username):
    db = app.config['db']
    return db.get_user(username)


if __name__ == "__main__":

    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port,debug=True)