import os
from os import path
from passlib.hash import pbkdf2_sha256 as hasher
import re

from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user

from entities.DataBase import get_User
from entities.Person import Person
from entities.Department import Department
from entities.Class import Class
from entities.Video import Video
from entities.Comment import Comment

from tools.utils import get_project_root, randomnamegen
from tools.uploadimage import uploadImage
from datetime import datetime

from forms import \
    CreateAccountForm, \
    ProfileUpdateForm, \
    LoginForm, \
    VideoUploadForm, \
    ClassSearchForm, \
    ClassCreateForm, \
    CommentPostForm, \
    DepartmentCreateForm, \
    StudentAddForm, \
    ClassUpdateForm, \
    VideoUpdateForm


def auth_page(info=False):
    form = LoginForm()

    if current_user.is_active is True:
        next_page = request.args.get("next", url_for("log_out"))
        return redirect(next_page)

    if form.validate_on_submit():
        if request.method == "GET":
            if info == "/SignUpSuccess":
                flash("Your account created successfully!","info")
            elif info=="/AccountCreateFailed":
                flash("Account Create Failed","error")

            return render_template("auth.html",form=form)
        else:
            username = request.form.get("username")
            password = request.form.get("password")

            if username == "" or password == "":
                flash("You can not leave blank space.","error")
                return render_template("auth.html",form=form)
         
            user = get_User(username)
            if user is not None:
                if hasher.verify(password, user.password):
                    if (user.account_type == "Tutor" and user.activated is True) or user.account_type != "Tutor":

                        user.logged_in = True
                        login_user(user)
                        next_page = request.args.get("next", url_for("profile_page",user=user.username))
                        return redirect(next_page)
                    else:
                        flash("Wait For Admin to Activate Your Account!!","error")
                        return redirect(url_for("auth_page"))

        flash("Your Log In informations are incorrect","error")
        return render_template("auth.html",form=form)
    
    return render_template("auth.html", form=form)


@login_required
def log_out():
    current_user.logged_in = False
    logout_user()
    flash("You have logged out.","info")
    return redirect(url_for("auth_page"))


def account_create_page():
    db = current_app.config["db"]
    form = CreateAccountForm()

    if form.validate_on_submit():
        username = form.data["username"]

        if db.CheckIfDataExists(username,"User"):
            flash("Username is already taken","error")
            return redirect(url_for("account_create_page"))

        password = form.data["password"]

        if len(password) < 3:
            flash("Please Use a password that is 10 or more than 10 characters","error")
            return redirect(url_for("account_create_page"))

        if len(password) > 20:
            flash("Please do not use any password that is more than 20 characters","error")
            return redirect(url_for("account_create_page"))

        if len(username) < 3:
            flash("Please Use a password that is 5 or more than 5 characters","error")
            return redirect(url_for("account_create_page"))

        if len(username) > 20:
            flash("Please do not use any password that is more than 20 characters","error")
            return redirect(url_for("account_create_page"))

        password = hasher.hash(password)
        id_number = form.data["id_number"]

        if db.CheckIfDataExists(id_number,"User_id"):
            flash("Id number in use by one user", "error")
            return redirect(url_for("account_create_page"))

        mail = form.data["mail"]

        if db.CheckIfDataExists(mail,"mail"):
            flash("Email is already taken", "error")
            return redirect(url_for("account_create_page"))

        account_type = form.data["account_type"]
        gender = form.data["gender"]
        department = form.data["department"]

        try:
            user = Person(
                id_number=id_number,
                username=username,
                password=password,
                department=department,
                account_type=account_type,
                gender=gender,
                mail=mail
            )
            db.create_user(user)
            if user.account_type == "Tutor":
                flash("Your account is created, wait for the admin, admin will activate your account.","info")
            return redirect(url_for("auth_page"))
        except:
            return render_template("accountcreate.html", form=form)

    return render_template("accountcreate.html", form=form)


@login_required
def profile_page(user):
    form = ProfileUpdateForm()

    user = current_user

    form.account_type.default = user.account_type
    form.gender.default = user.gender
    form.department.default = user.department

    form.process()
    db = current_app.config["db"]

    if user.account_type == "Tutor":
        db = current_app.config["db"]
        db.update_most_reviewed_video(user.id_number)

    most_viewed_video = None
    if user.account_type == "Tutor":
        most_viewed_video = db.get_most_viewed_video(user.most_viewed_video)

    if form.validate_on_submit():

        if request.form["update"] == "Update Profile Information":
            return render_template("profile.html", user=user, form=form, update=True)

        if request.form["update"] == "Save Changes":
            image_file = request.files["image"]
            gender = request.form.get("gender")
            user_name = request.form.get("username")
            password = request.form.get("password")
            department = request.form.get("department")
            mail = request.form.get("mail")
            title = request.form.get("title")

            if gender == "":
                gender = None

            if user_name == "":
                user_name = None

            if password == "":
                password = None

            if department == "":
                department = None

            if mail == "":
                mail = None

            if title == "":
                title = None

            user.set_user(
                username=user_name,
                password=hasher.hash(password) if password is not None else None,
                gender=gender,
                department=department,
                mail=mail,
                title=title
            )

            if image_file.read() != b'':

                if image_file.content_type.split('/')[0] == "image":
                    temp = current_user.profileimage
                    temp = temp.replace("../static/profile_images/","")
                    prev_image = str(get_project_root())+"\\static\\profile_images\\"+temp

                    if temp != "boy.png" and temp != "girl.png":
                        if path.exists(prev_image):
                            os.remove(prev_image)

                    user.profileimage = uploadImage(image_file.stream, user.id_number)
                    user.convert_image_path()
                    current_user.profileimage = user.profileimage

                db.update_user_info(user.id_number, user)

                if user_name is None and image_file.content_type.split('/')[0] != "image":
                    flash(f"Please Upload an Image instead of a {image_file.content_type.split('/')[1]} file!",
                          "error")
                    return redirect(url_for("profile_page", user=user.username))

            if user_name is not None:
                flash("You changed your username. You have to reloggin to your account.","info")
                return redirect(url_for('auth_page'))

    return render_template("profile.html", user=user, form=form, update=False, department_name=current_app.config['db'].get_departments(user.department).department_name, most_viewed_video=most_viewed_video)


@login_required
def personal_classes_page(user):
    db = current_app.config["db"]
    user = current_user
    tutor = ""
    tutor_list = []

    if user.account_type == "Tutor":
        tutor, class_list = db.get_tutors_classes(user.id_number)
    elif user.account_type == "Student":
        tutor_list, class_list = db.get_students_classes(user.id_number)
    else:
        return redirect(url_for("profile_page",user=user.username))

    return render_template("classes.html", user=user, personal=True, tutor=tutor, tutor_list=tutor_list, db=db, class_list=class_list)


def validate_class_code(field):
    match = re.compile('[A-Z][A-Z][A-Z]' + '-' + '[0-9][0-9][0-9][A-Z]' + '-' + '[0-9][0-9][0-9]')
    m = re.match(match, field)
    if not m:
        return False
    else:
        return True


@login_required
def create_class_page():
    user = current_user

    if user.account_type != "Tutor":
        return redirect(url_for("profile_page",user=user.username))

    db = current_app.config["db"]
    form = ClassCreateForm()

    if form.validate_on_submit():
        class_name = request.form.get("class_name")
        class_code = request.form.get("class_code")
        class_department = request.form.get("department")
        class_context = request.form.get("class_context")
        class_capacity = request.form.get("class_capacity")

        if not validate_class_code(class_code):
            flash("Please Give A proper class code, class code should be in this type ABC-123A-123","error")
            return redirect(url_for("create_class_page"))

        if class_department == "None":
            flash("Please Choose a Deparment!","error")
            return redirect(url_for("create_class_page"))

        if len(class_name) > 70 or len(class_name) < 3:
            flash("Please Use a Class name that is less than or equal to 70 characters or greater then or equal to 3")
            return redirect(url_for("create_class_page"))

        nclass = Class(class_name, class_code, user.id_number, class_context=class_context, class_capacity=class_capacity,department=class_department)

        if db.create_class(nclass) == "Class code exists":
            flash("Class Code Already Exists!","error")
            return redirect(url_for("create_class_page"))

        flash("Class Created Successfully","info")
        return redirect(url_for("create_class_page"))

    return render_template("./tutor/classcreatepage.html", user=user, form=form)


@login_required
def upload_video_page(user):
    form = VideoUploadForm()
    user = current_user

    if user.account_type != "Tutor":
        return redirect(url_for("profile_page", user=user))

    db = current_app.config["db"]

    if form.validate_on_submit():
        thumbnail = request.files['video_thumbnail']
        video = request.files['video']
        video_title = request.form.get("video_title")
        video_class = request.form.get("video_class")
        video_comments_available = request.form.get("video_comments_available")
        video_descriptions = request.form.get("video_descriptions")
        print("burak")
        if len(video_title) > 200 or len(video_title) < 5:
            print("len")
            flash("Please use a video title between 5 and 200 characters", "error")
            return redirect(url_for("upload_video_page", user=user.username))

        if video.filename != '' and thumbnail != '':
            print("hELLO")
            if video.content_type.split('/')[0] != "video":
                print("hELLO video")

                flash("Please add a proper file to video section","error")
                return redirect(url_for("upload_video_page", user=user.username))

            if thumbnail.content_type.split('/')[0] != "image":
                print("hELLO image")

                flash("Please add a proper file to image section", "error")
                return redirect(url_for("upload_video_page", user=user.username))

            video_path = "./static/videos/" + randomnamegen(100) + "-" + \
                         video_class + "." + \
                         video.content_type.split('/')[1]
            video.save(video_path)

            thumbnail_path = "./static/video_thumbnail/" + randomnamegen(100) + "-" + \
                         video_class + "." + \
                         thumbnail.content_type.split('/')[1]
            thumbnail.save(thumbnail_path)

            nvideo = Video(video_title, randomnamegen(20), user.id_number, video_class, None,
                          thumbnail_path, video_path, video_descriptions, video_comments_available)


            db.create_video(nvideo)

            flash("Video Uploaded Successfully","info")
            return redirect(url_for("upload_video_page",user=user.username))

        flash("Please fill the necessary places!")
        return render_template("videoupload.html", form=form, user=user)

    return render_template("videoupload.html", form=form, user=user)


@login_required
def all_classes_page():
    form = ClassSearchForm()
    user = current_user

    db = current_app.config["db"]

    tutor_list, class_list = db.get_all_classes()

    if form.validate_on_submit():
        department = request.form.get("department")

        if department == "0":
            department = None

        tutor = request.form.get("tutor")

        if tutor == "0":
            tutor = None

        star = request.form.get("stars")

        tutor_list, class_list = db.search_classes(department,tutor,star)

        return render_template("classes.html", form=form, user=user, db=db, personal=False,tutor_list=tutor_list, class_list=class_list)
    
    return render_template("classes.html", form=form, user=user, db=db, personal=False,tutor_list=tutor_list, class_list=class_list)


@login_required
def class_page(class_code):
    user = current_user
    db = current_app.config["db"]

    if user.account_type == "Student":
        if not db.check_student_in_class(user.id_number, class_code):
            flash("You are not in this class")
            return redirect(url_for("profile_page", user=user.username))

    nclass, tutor = db.get_class_with_class_code(class_code)
    video_list = db.get_videos(class_code)

    for video in video_list:
        video.convert_image_path()

    return render_template("classpage.html", user=user, video_list=video_list, tutor=tutor, nclass=nclass)

@login_required
def delete_class(class_code):
    if current_user.account_type != "admin":
        return redirect(url_for("profile_page", user=current_user.username))

    db = current_app.config["db"]
    db.delete_class(class_code)
    return redirect(url_for("all_classes_page"))


@login_required
def video_page(class_code, video_code):
    form = CommentPostForm()
    user = current_user
    db = current_app.config["db"]

    if db.check_video_reviewed(video_code, user.id_number):
        form.review_points.render_kw = {'disabled' : 'disabled'}

    if user.account_type == "Student":
        if not db.check_student_in_class(user.id_number, class_code):
            flash("You are not in this class")
            return redirect(url_for("profile_page", user=user.username))

    comment_list = db.get_comments(video_code)
    tutor, video = db.get_video_with_video_code(video_code)

    video.convert_video_path()
    video.convert_image_path()

    if video.comments_available is not True:
        form.comment.render_kw = {'disabled': 'disabled'}
        form.send_comment.render_kw = {'disabled': 'disabled'}

    if form.validate_on_submit():
        review_point = request.form.get("review_points")

        if review_point != "0" and not db.check_video_reviewed(video_code, user.id_number):
            db.add_review_point(review_point, video_code, user.id_number)

        comment = request.form.get("comment")

        time = datetime.date(datetime.now())

        if comment != "":
            comment = Comment(
                comment_id=randomnamegen(50),
                user_id=user.id_number,
                video_code=video_code,
                comment_context=comment,
                time=time
            )
            db.create_comment(comment)

        return redirect(url_for("video_page", class_code=class_code, video_code=video_code))

    return render_template("videopage.html", form=form, tutor=tutor, video=video, user=user, db=db, comment_list=comment_list)


@login_required
def admin_panel_page():

    if current_user.account_type != "admin":
        return redirect(url_for("profile_page", user=current_user.username))

    db = current_app.config['db']

    return render_template("./admin/adminpage.html", user=current_user, Users=db.get_all_users())



@login_required
def admin_users_page():
    if current_user.account_type != "admin":
        return redirect(url_for("profile_page", user=current_user.username))

    db = current_app.config['db']

    return render_template("./admin/adminuserspage.html", user=current_user, Users=db.get_all_users())


@login_required
def user_delete(user_id):
    if current_user.account_type != "admin":
        return redirect(url_for("profile_page", user=current_user.username))

    db = current_app.config["db"]
    db.delete_user(user_id)
    return redirect(url_for("admin_users_page"))

@login_required
def user_activate(user_id):
    if current_user.account_type != "admin":
        return redirect(url_for("profile_page", user=current_user.username))

    db = current_app.config["db"]
    db.activate_user(user_id)
    return redirect(url_for("admin_users_page"))


@login_required
def department_page():
    if current_user.account_type != "admin":
        return redirect(url_for("profile_page", user=current_user.username))

    db = current_app.config["db"]
    department_list = db.get_departments()

    form = DepartmentCreateForm()
    if form.validate_on_submit():
        department_name = request.form.get("department_name")
        department_code = request.form.get("department_code").upper()

        if len(department_name) > 50 and len(department_name) < 5:
            flash("Please use a department name that is more than 5 characters and less then 50 characters", "error")
            return redirect(url_for("department_page"))

        if len(department_code) > 10 and len(department_code) < 2:
            flash("Please use a department code that is more than 2 characters and less then 10 characters", "error")
            return redirect(url_for("department_page"))

        department = Department(department_code, department_name)
        code_exist, name_exist = db.check_if_department_exists(department)
        if not code_exist and not name_exist:
            db.create_department(department)
        elif code_exist:
            flash(f"Department Code {department_code} is already exist!","error")
        elif name_exist:
            flash(f"Department Name {department_name} is already exist!", "error")


        return redirect(url_for("department_page"))

    return render_template("./admin/departmentspage.html", user=current_user, form=form, department_list=department_list)

@login_required
def department_delete(department_code):
    if current_user.account_type != "admin":
        return redirect(url_for("profile_page", user=current_user.username))

    db = current_app.config["db"]
    db.delete_department(department_code)
    return redirect(url_for("department_page"))

@login_required
def student_add_page(class_code):
    if current_user.account_type != "Tutor":
        return redirect(url_for("profile_page", user=current_user.username))

    db = current_app.config["db"]
    form = StudentAddForm(class_code)

    student_list = db.get_all_students_from_class(class_code)

    nclass, tutor = db.get_class_with_class_code(class_code)
    if form.validate_on_submit():
        students = request.form.getlist("student")

        capacity = request.form.get("capacity")
        if capacity != "":
            db.update_capacity_of_a_class(class_code,capacity)
        if nclass.number_of_students < nclass.class_capacity:
            db.add_student(students, class_code)
        else:
            flash("Class Capacity is Full!", "alert-error")

        return redirect(url_for("student_add_page",class_code=class_code))

    return render_template("./tutor/studentadd.html", nclass=nclass, form=form, user=current_user, student_list=student_list)

@login_required
def delete_student_from_class(class_code, student_id):
    if current_user.account_type != "Tutor":
        return redirect(url_for("profile_page", user=current_user.username))

    db = current_app.config["db"]
    db.delete_student_from_class(class_code,student_id)
    flash(f"student with {student_id} id deleted!","info")
    return redirect(url_for("student_add_page",class_code=class_code))

@login_required
def tutor_list():
    db = current_app.config["db"]

    return render_template("./admin/adminuserspage.html", user=current_user, Users=db.get_tutors())

@login_required
def delete_video(class_code,video_code):
    if current_user.account_type == "Student":
        return redirect(url_for("profile_page",user=current_user.user_name))

    db = current_app.config["db"]
    db.delete_video(video_code)
    return redirect(url_for("class_page", class_code=class_code))

@login_required
def update_class_page(class_code):
    if current_user.account_type != "Tutor":
        return redirect(url_for("profile_page",user=current_user.user_name))

    form = ClassUpdateForm()

    db = current_app.config["db"]

    if form.validate_on_submit():
        class_name = request.form.get("class_name")
        nclass_code = request.form.get("class_code")
        class_context = request.form.get("class_context")

        if not validate_class_code(nclass_code):
            flash("Please Give A proper class code, class code should be in this type ABC-123A-123","error")
            return redirect(
                url_for("update_class_page", class_code=nclass_code if nclass_code is not None else class_code))

        if class_name == "":
            class_name = None

        if nclass_code == "":
            nclass_code = None

        if class_context == "":
            class_context = None

        nclass = Class(class_name,nclass_code,None,None,class_context)
        db.update_class_with_class_code(class_code,nclass)
        flash("Class Updated","info")
        return redirect(url_for("update_class_page",class_code=nclass_code if nclass_code is not None else class_code ))

    return render_template("./tutor/classupdatepage.html", user=current_user, form=form)


@login_required
def update_video_page(class_code, video_code):
    form = VideoUpdateForm()

    if current_user.account_type != "Tutor":
        return redirect(url_for("profile_page",user=current_user.user_name))

    db = current_app.config["db"]

    t_tutor, t_video = db.get_video_with_video_code(video_code)

    if form.validate_on_submit():
        thumbnail = request.files['video_thumbnail']
        video = request.files['video']
        video_title = request.form.get("video_title")
        video_class = request.form.get("video_class")
        video_comments_available = request.form.get("video_comments_available")
        video_descriptions = request.form.get("video_descriptions")
        thumbnail_path = ""
        video_path = ""

        if len(video_title) > 200 or len(video_title) < 5:
            flash("Please use a video title between 5 and 200 characters", "error")
            return redirect(url_for("upload_video_page", user=current_user.username))

        if thumbnail == '':
            thumbnail = None
            thumbnail_path = None

        if video.filename == '':
            video.filename = None
            video_path = None

        if video_title == '':
            video_title = None

        if video_class == '':
            video_class = None

        if video_comments_available is None:
            video_comments_available = False

        if video_descriptions == '':
            video_descriptions = None

        if video.filename is not None :
            video_path = "./static/videos/" + randomnamegen(100) + "-" + \
                         video_class + "." + \
                         video.content_type.split('/')[1]
            os.remove(t_video.video_path)
            video.save(video_path)

        if thumbnail is not None:
            thumbnail_path = "./static/video_thumbnail/" + randomnamegen(100) + "-" + \
                             video_class + "." + \
                             thumbnail.content_type.split('/')[1]
            os.remove(t_video.thumbnail_path)
            thumbnail.save(thumbnail_path)

        nvideo = Video(video_title, None, current_user.id_number, video_class, None,
                       thumbnail_path, video_path, video_descriptions, video_comments_available)

        db.update_video_with_video_code(video_code, nvideo)

        flash("Video Updated","info")
        return redirect(url_for("update_video_page", user=current_user.username, video_code=video_code,class_code=class_code))

    return render_template("./tutor/videoupdate.html",user=current_user, form=form, video_name=t_video.video_name)


@login_required
def student_comments_page(user):
    user = current_user
    db = current_app.config["db"]
    video_list = db.get_student_comments(user.id_number)
    return render_template("studentcomments.html",user=user, video_list=video_list)