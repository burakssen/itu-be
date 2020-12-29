from flask import Flask, render_template, request, redirect, url_for, flash, current_app,abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from io import BytesIO

from tools.uploadimage import uploadImage
from forms import CreateAccountForm, ProfileUpdateForm, LoginForm, VideoUploadForm, ClassSearchForm
from passlib.hash import pbkdf2_sha256 as hasher
from entities.Entities import DataBase, Person, Class, Video, get_User

image = ""
def auth_page(info=False):
    form = LoginForm()
    
    if form.validate_on_submit():
        if request.method == "GET":
            if info == "#/SignUpSuccess":
                flash("Your account created successfully!","info")
            elif info=="#/AccountCreateFailed":
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
                    login_user(user)
                    next_page = request.args.get("next", url_for("profile_page",user=user.username))
                    return redirect(next_page)
                    
        flash("Your Log In informations are incorrect","error")
        return render_template("auth.html",form=form)
    
    return render_template("auth.html", form=form)

def log_out():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("auth_page"))

def account_create_page():
    db = DataBase("Itu-be","burakssen", "18Kalemlik09.")
    form = CreateAccountForm()
    if form.validate_on_submit():
        username = form.data["username"]
        password = form.data["password"]
        password = hasher.hash(password)
        id_number = form.data["id_number"]
        mail = form.data["mail"]
        account_type = "admin"
        gender = form.data["gender"]
        department = form.data["department"]
        print(department)
        try:
            user = Person(username, id_number, mail, account_type, gender, department, password)
            db.create_user(user)
        except:
            return redirect(url_for("auth_page", ))

    return render_template("accountcreate.html",form=form)

@login_required
def profile_page(user):
    form = ProfileUpdateForm()
    user = current_user
    form.account_type.default = user.account_type

    form.process()
    if form.validate_on_submit():

        if request.form["update"] == "Update Profile Information":
            return render_template("profile.html", user=user, form=form, update=True)

        if request.form["update"] == "Save Changes":
            image_file = form.image.data
            gender = request.form.get("gender")
            val = request.form.get("faculty")
            faculty = dict(form.faculty.choices).get(val)
            user.set_user(gender=gender,faculty=faculty)
            if image_file != None:
                user.profileimage = uploadImage(BytesIO(image_file.read()),user.id_number)
    
    return render_template("profile.html", user=user, form=form, update=False, department_name=current_app.config['db'].get_departments(user.department)[0].department_name)
   
@login_required
def upload_video_page(user):
    form = VideoUploadForm()
    user = Person(user,"admin","Male","Computer and Informatics Engineering")

    if form.validate_on_submit():
        if request.method == "POST":
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.save(uploaded_file.filename)
                return redirect(url_for('videupload'), form=form, user=user)

        render_template("videoupload.html",form=form, user=user)

    return render_template("videoupload.html",form=form, user=user)
    
@login_required
def classes_page():
    form = ClassSearchForm()
    user = Person("burakssen","admin","Male","Computer and Informatics Engineering")
    classList = []
    for i in range(10):
        cs = Class("Database Systems","BLG 317E","Ali Çakmak","Computer Science and Informatics","Computer Science and Informatics",5)
        classList.append(cs)

    if form.validate_on_submit():
        return render_template("classes.html", form=form, user=user, classList=classList)
    
    return render_template("classes.html", form=form, user=user, classList=classList)

@login_required
def class_page(classCode):

    user = Person("burakssen","admin","Male","Computer and Informatics Engineering")
    videoList = []

    for i in range(10):
        vi = Video("Normalization",i,"Ali Çakmak","Computer Engineering",5,"../static/profile_images/boy.png","../help")
        videoList.append(vi)
        

    return render_template("classpage.html", user=user, videoList=videoList, classCode=classCode)

@login_required
def video_page(classCode, videoCode):
    user = Person("burakssen","admin","Male","Computer and Informatics Engineering")
    return render_template("videopage.html", user=user)

@login_required
def admin_panel_page():
    if current_user.account_type != "admin":
        return redirect(url_for("profile_page",user=current_user.user_name))

    return render_template("./admin/adminpage.html", user=current_user, Users=[])

@login_required
def admin_users_page():
    pass
    