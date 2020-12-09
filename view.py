from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, current_app
from flask_login import login_user, login_required
from io import BytesIO
from werkzeug.utils import secure_filename

from tools.uploadimage import uploadImage
from forms import CreateAccountForm, ProfileUpdateForm, LoginForm, VideoUploadForm, ClassSearchForm
from tools.hash import hash_password, hash_control
from entities.person import Person
from entities.Class import Class


image = ""
id = 0

def auth_page(info=False):
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == "GET":
            if info == "#/SignUpSuccess":
                flash("Your account created successfully!","info")
            return render_template("auth.html",form=form)
        else:
            username = request.form.get("username")
            password = request.form.get("password")
        
        
            if username == "" or password == "":
                flash("You can not leave blank space.","error")
                return render_template("auth.html",form=form)
                
                #TODO return redirect(next or url_for("profile_page",username=username))

        flash("Your Log In informations are incorrect","error")
        return render_template("auth.html",form=form)
    
    return render_template("auth.html", form=form)

def account_create_page():
    form = CreateAccountForm()
    if form.validate_on_submit():
        username = form.data["username"]
        password = form.data["password"]
        
        return redirect(url_for("profile_page", username=username))

    return render_template("accountcreate.html",form=form)

def profile_page(user):
    global image
    global id
    form = ProfileUpdateForm()
    user = Person(user,"admin","Male","Computer and Informatics Engineering")
    form.account_type.default = user.account_type
    form.process
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
                user.profileimage = uploadImage(BytesIO(image_file.read()),id)
                print(image)
                id+=1  
    
    return render_template("profile.html", user=user, form=form, update=False)
   

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
    
   
def classes_page():
    form = ClassSearchForm()
    user = Person("burakssen","admin","Male","Computer and Informatics Engineering")
    classList = []
    for i in range(10):
        cs = Class(i*i,i,i+i+i+i,"!!!!","a"*i,5)
        classList.append(cs)

    if form.validate_on_submit():
        return render_template("classes.html", form=form, user=user, classList=classList)
    
    return render_template("classes.html", form=form, user=user, classList=classList)
    