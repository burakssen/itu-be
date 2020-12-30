from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SelectMultipleField, SelectField, SubmitField, BooleanField, \
    TextAreaField, RadioField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField
from flask import current_app


class CreateAccountForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = current_app.config["db"]
        self.department.choices = [
            (department.department_code, department.department_name) for department in self.db.get_departments()
        ]

    username = StringField("Username", validators=[DataRequired()])

    id_number = IntegerField("Id", validators=[DataRequired(), NumberRange(min=99999999, max=999999999)])

    password = PasswordField("Password", validators=[DataRequired()])

    mail = StringField("Mail", validators=[DataRequired()])

    account_type = SelectField("Account Type", validators=[DataRequired()], choices=["Admin","Student", "Tutor"])

    department = SelectField("department", validators=[DataRequired()],
                             choices=[],
                             validate_choice=[]
                             )

    gender = SelectField("Gender", choices=["Male", "Female"])


class LoginForm(FlaskForm):
    username = StringField("Username")

    password = PasswordField("Password")

    loginbutton = SubmitField("Log In")


class ProfileUpdateForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = current_app.config["db"]
        self.department.choices = [
            (department.department_code, department.department_name) for department in self.db.get_departments()
        ]

    update = SubmitField("Update")

    username = StringField("Username", validators=[Optional()])

    password = PasswordField("Password", validators=[Optional()])

    id_number = IntegerField("Id Number", validators=[Optional()])

    gender = SelectField("Gender", choices=["Male", "Female"], validators=[Optional()])

    mail = StringField("Mail", validators=[Optional()])

    image = FileField("image", validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'Only PNG, JPG and JPEG Allowed!')])

    account_type = SelectField("Account Type", choices=["Admin", "Tutor", "Student"], validators=[Optional()])

    department = SelectField("Department",coerce=str, validators=[Optional()], choices=[],validate_choice=[])


class VideoUploadForm(FlaskForm):
    video_thumbnail = FileField("image",
                                validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only PNG, JPG and JPEG Allowed!')])

    video = FileField("video", validators=[FileAllowed(['mp4', '3gp', 'mkv'], 'Only mp4, 3gp and mkv Allowed!')])

    video_title = StringField("Video Title")

    video_class = SelectField()

    video_comments_available = BooleanField("Available")

    video_descriptions = TextAreaField("Descriptions", render_kw={"rows": 12, "cols": 50}, validators=[Optional()])


class ClassSearchForm(FlaskForm):
    class_name = StringField("Class Name")

    class_code = SelectField()

    tutor = SelectField()

    stars = RadioField("Stars", choices=[5, 4, 3, 2, 1])
