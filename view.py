import os
from os import path
from passlib.hash import pbkdf2_sha256 as hasher

from flask import render_template, request, redirect, url_for, flash, current_app, session
from flask_login import login_user, logout_user, login_required, current_user

from entities.DataBase import get_User
from entities.Person import Person
from entities.Department import Department
from entities.Class import Class
from entities.Video import Video
from entities.Comment import Comment

from tools.utils import get_project_root, randomnamegen
from tools.uploadimage import uploadImage

from forms import \
    CreateAccountForm, \
    ProfileUpdateForm, \
    LoginForm, \
    VideoUploadForm, \
    ClassSearchForm, \
    ClassCreateForm, \
    CommentPostForm, \
    DepartmentCreateForm, \
    StudentAddForm


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
                    user.logged_in = True
                    login_user(user)
                    next_page = request.args.get("next", url_for("profile_page",user=user.username))
                    return redirect(next_page)

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
            return redirect(url_for("auth_page"))
        except:
            return render_template("accountcreate.html", form=form)
    return render_template("accountcreate.html", form=form)


@login_required
def access_denied():
    return redirect(url_for("profile_page", user=current_user.username))


@login_required
def profile_page(user):
    form = ProfileUpdateForm()

    user = current_user

    form.account_type.default = user.account_type
    form.gender.default = user.gender
    form.department.default = user.department

    form.process()
    db = current_app.config["db"]
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

            user.set_user(
                username=user_name if user_name != "" else user.username,
                password=hasher.hash(password) if password != "" else user.password,
                gender=gender if gender != "" else user.gender,
                department=department if department != "" else user.department,
                mail=mail if mail != "" else user.mail,
                title=title if title != "" else user.title
            )

            if image_file.read() != b'':
                temp = current_user.profileimage
                temp = temp.replace("../static/profile_images/","")
                prev_image = str(get_project_root())+"\\static\\profile_images\\"+temp

                if temp != "boy.png" and temp != "girl.png":
                    if path.exists(prev_image):
                        os.remove(prev_image)

                user.profileimage = uploadImage(image_file.stream, user.id_number)
                user.convert_image_path()
                current_user.profile_image = user.profileimage
            else:
                user.set_profile_image()
                current_user.profile_image = user.profileimage

            db.update_user_info(user.id_number, user)

    return render_template("profile.html", user=user, form=form, update=False, department_name=current_app.config['db'].get_departments(user.department).department_name)


@login_required
def tutor_classes_page(user):
    db = current_app.config["db"]
    user = current_user
    tutor, class_list = db.get_tutors_classes(user.id_number)
    return render_template("classes.html", user=user, personal=True, tutor=tutor,db=db, class_list=class_list)


@login_required
def create_class_page(info=None):
    user = current_user

    if user.account_type != "Tutor":
        return redirect(url_for("profile_page",user=user.username))

    db = current_app.config["db"]
    form = ClassCreateForm()

    flash("help")

    if form.validate_on_submit():
        class_name = request.form.get("class_name")
        class_code = request.form.get("class_code")
        class_context = request.form.get("class_context")
        class_capacity = request.form.get("class_capacity")

        nclass = Class(class_name, class_code, user.id_number, class_context=class_context, class_capacity=class_capacity)

        if db.create_class(nclass) == "Class code exists":
            return redirect(url_for("create_class_page", info="fail"))

        return redirect(url_for("create_class_page", info="success"))

    return render_template("./tutor/classcreatepage.html", user=user, form=form, info=info)


@login_required
def upload_video_page(user, info=None):
    form = VideoUploadForm()
    user = current_user

    if user.account_type != "Tutor":
        return redirect(url_for("profile_page", user=user))

    db = current_app.config["db"]

    if info == "success":
        flash("You created uploaded a video","info")

    if form.validate_on_submit():
        thumbnail = request.files['video_thumbnail']
        video = request.files['video']
        video_title = request.form.get("video_title")
        video_class = request.form.get("video_class")
        video_comments_available = request.form.get("video_comments_available")
        video_descriptions = request.form.get("video_descriptions")

        if video.filename != '' and thumbnail != '':
            video_path = ".\\"+str(get_project_root()) + \
                         "\\static\\videos\\" + \
                         randomnamegen(100) + "-" + \
                         video_class + "." + \
                         video.content_type.split('/')[1]
            video_path = video_path.replace("\\", "/")
            video.save(video_path)

            thumbnail_path = str(get_project_root()) + \
                        "\\static\\video_thumbnail\\" + \
                        randomnamegen(100) + "-" + \
                        video_class + "." + \
                        thumbnail.content_type.split('/')[1]
            thumbnail_path = thumbnail_path.replace("\\", "/")

            thumbnail.save(thumbnail_path)

            nvideo = Video(video_title, randomnamegen(20), user.id_number, video_class, None,
                          thumbnail_path, video_path, video_descriptions, video_comments_available)


            db.create_video(nvideo)

            return redirect(url_for("upload_video_page",user=user.username, info="success"))

        return render_template("videoupload.html", form=form, user=user)

    return render_template("videoupload.html", form=form, user=user)


@login_required
def all_classes_page(filtered=None):
    form = ClassSearchForm()
    user = current_user

    db = current_app.config["db"]

    tutor_list, class_list = db.get_all_classes()


    if form.validate_on_submit():
        department = request.form.get("department")

        tutor = request.form.get("tutor")

        star = request.form.get("stars")

        return render_template("classes.html", form=form, user=user, db=db, personal=False,tutor_list=tutor_list, class_list=class_list)
    
    return render_template("classes.html", form=form, user=user, db=db, personal=False,tutor_list=tutor_list, class_list=class_list)


@login_required
def class_page(class_code):
    user = current_user
    db = current_app.config["db"]
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

    comment_list = db.get_comments(video_code)
    tutor, video = db.get_video_with_video_code(video_code)

    video.convert_video_path()
    video.convert_image_path()

    if form.validate_on_submit():
      comment = request.form.get("comment")

      if comment != "":
        comment = Comment(
            comment_id=randomnamegen(50),
            user_id=user.id_number,
            video_code=video_code,
            comment_context=comment
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

    return render_template("./admin/adminuserspage.html", user=current_user,db=db, Users=db.get_all_users())


@login_required
def user_delete(user_id):
    if current_user.account_type != "admin":
        return redirect(url_for("profile_page", user=current_user.username))

    db = current_app.config["db"]
    db.delete_user(user_id)
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
        department_code = request.form.get("department_code")

        department = Department(department_code, department_name)
        db.create_department(department)

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
def delete_student_from_class(class_code,student_id):
    if current_user.account_type != "Tutor":
        return redirect(url_for("profile_page", user=current_user.username))


    db = current_app.config["db"]
    db.delete_student_from_class(class_code,student_id)
    return redirect(url_for("student_add_page",class_code=class_code))