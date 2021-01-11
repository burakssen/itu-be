from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SelectMultipleField, SelectField, SubmitField, BooleanField, \
    TextAreaField, RadioField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from wtforms_components import IntegerField
from flask import current_app
from flask_login import current_user


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

    account_type = SelectField("Account Type", validators=[DataRequired()], choices=["Student", "Tutor"])

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

    title = StringField("Title", validators=[Optional()])


class VideoUploadForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = current_app.config["db"]
        self.video_class.choices = [
            (nclass.class_code, f"{nclass.class_code}: {nclass.class_name}") for nclass in self.db.get_tutors_classes(current_user.id_number)
        ]
    video_thumbnail = FileField("image",
                                validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only PNG, JPG and JPEG Allowed!'), Optional()])

    video = FileField("video", validators=[FileAllowed(['mp4', '3gp', 'mkv'], 'Only mp4, 3gp and mkv Allowed!')])

    video_title = StringField("Video Title")

    video_class = SelectField("Video Class")

    video_comments_available = BooleanField("Available")

    video_descriptions = TextAreaField("Descriptions", render_kw={"rows": 12, "cols": 50}, validators=[Optional()])


class ClassSearchForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = current_app.config["db"]
        self.department.choices = [
            (department.department_code, department.department_name) for department in self.db.get_departments()
        ]

        tutors_list = []

        for user in self.db.get_all_users():
            if user.account_type == "Tutor":
                tutors_list.append(user)

        self.tutor.choices = [
            (ntutor.id_number, ntutor.username) for ntutor in tutors_list
        ]


    department = SelectField("Department")

    tutor = SelectField("Tutors")

    stars = RadioField("Stars", choices=[(5,5), (4,4), (3,3), (2,2), (1,1)])


class ClassCreateForm(FlaskForm):
    class_name = StringField("Class Name")

    class_code = StringField("Class Code")

    class_capacity = IntegerField("Class Capacity",validators=[NumberRange(min=5, max=40)])

    class_context = TextAreaField("Class Context", render_kw={"rows": 12, "cols": 50}, validators=[Optional()])

    create_button = SubmitField("Create Class")


class CommentPostForm(FlaskForm):
    comment = TextAreaField("Comment", render_kw={"rows": 5, "cols": 48}, validators=[Optional()])

    send_comment = SubmitField("Comment!")


class DepartmentCreateForm(FlaskForm):
    department_name = StringField("Department Name")

    department_code = StringField("Department Code")

    create_button = SubmitField("Create Department")


class StudentAddForm(FlaskForm):
    def __init__(self, class_code=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = current_app.config["db"]
        student_list = self.db.get_all_student()

        self.student.choices = [
            (student.id_number, f"{student.id_number}: {student.username} -- This Student is already in the class" if self.db.check_if_student_in_the_class(class_code,student.id_number) else f"{student.id_number}: {student.username}") for student in student_list
        ]

    student = SelectMultipleField("Student", choices=[], coerce=int)

    submit_button = SubmitField("Add Students")

    capacity = IntegerField("Capacity", validators=[Optional(), NumberRange(min=5,max=60)])