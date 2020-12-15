from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SelectMultipleField, SelectField, SubmitField, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField

class CreateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])

    id_number = IntegerField("Id", validators=[DataRequired(), NumberRange(min=99999999, max=999999999)])

    password = PasswordField("Password", validators=[DataRequired()])

    mail = StringField("Mail", validators=[DataRequired()])

    account_type = SelectField("Account Type",validators=[DataRequired()],choices=["Student", "Tutor"])

    faculty = SelectField("Faculty", validators=[DataRequired()],
        choices=["Civil Engineering", "Computer and Informatics Engineering","Electrical and Electronic Engineering"],
        validate_choice=["CE","CIE","EEE"]
    )
    
    gender = SelectField("Gender", choices=["Male","Female"])

class LoginForm(FlaskForm):
    username = StringField("Username")

    password = PasswordField("Password")

    loginbutton = SubmitField("Log In")

class ProfileUpdateForm(FlaskForm):
    update = SubmitField("Update")

    username = StringField("Username")

    password = PasswordField("Password")

    id_number = IntegerField("Id Number")
    
    gender = SelectField("Gender", choices=["Male","Female"],validate_choice=["M,F"],validators=[Optional()])
    
    mail = StringField("Mail")

    image = FileField("image",validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only PNG, JPG and JPEG Allowed!')])

    account_type = SelectField("Account Type",choices=["Admin", "Tutor", "Student"],validators=[Optional()])

    faculty = SelectField("Faculty",
        choices=[("CE","Civil Engineering"), ("CIE","Computer and Informatics Engineering"),("EEE","Electrical and Electronic Engineering")],
        validators=[Optional()]
    )


class VideoUploadForm(FlaskForm):
    video_thumbnail = FileField("image",validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only PNG, JPG and JPEG Allowed!')])
    
    video = FileField("video", validators=[FileAllowed(['mp4', '3gp', 'mkv'], 'Only mp4, 3gp and mkv Allowed!')])

    video_title = StringField("Video Title")

    video_class = SelectField()

    video_comments_available = BooleanField("Available")

    video_descriptions = TextAreaField("Descriptions", render_kw={"rows": 12, "cols": 50}, validators=[Optional()])
    

class ClassSearchForm(FlaskForm):
    class_name = StringField("Class Name")

    class_code = SelectField()

    tutor = SelectField()

    stars = RadioField("Stars",choices=[5,4,3,2,1])    