from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SelectMultipleField, SelectField, SubmitField
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

#TODO
class LoginForm(FlaskForm):
    pass

class ProfileUpdateForm(FlaskForm):
    update = SubmitField("Update")

    username = StringField("Username")

    password = PasswordField("Password")

    id_number = IntegerField("Id Number")
    
    gender = SelectField("Gender", choices=["Male","Female"],validate_choice=["M,F"],validators=[Optional()])
    
    mail = StringField("Mail")

    image = FileField("image",validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only PNG, JPG and JPEG Allowed!')])

    account_type = SelectField("Account Type",choices=["Student", "Tutor"],validators=[Optional()])

    faculty = SelectField("Faculty",
        choices=["Civil Engineering", "Computer and Informatics Engineering","Electrical and Electronic Engineering"],
        validate_choice=["CE","CIE","EEE"],
        validators=[Optional()]
    )

    