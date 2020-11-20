from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField

class CreateAccountForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])

    id_number = IntegerField("id", validators=[DataRequired(), NumberRange(min=99999999, max=999999999)])

    password = PasswordField("password", validators=[DataRequired()])

    mail = StringField("mail", validators=[DataRequired()])

    account_type = SelectField("account_type",validators=[DataRequired()],choices=["Student", "Tutor"])

    faculty = SelectField("faculty", validators=[DataRequired()],
        choices=["Civil Engineering", "Computer and Informatics Engineering","Electrical and Electronic Engineering"],
        validate_choice=["CE","CIE","EEE"]
    )

#TODO
class LoginForm(FlaskForm):
    pass
