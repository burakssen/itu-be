from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, current_app
from flask_login import login_user, login_required
from io import BytesIO
from werkzeug.utils import secure_filename

from tools.uploadimage import uploadImage
from forms import CreateAccountForm, ProfileUpdateForm
from tools.hash import hash_password, hash_control

image = ""
id = 0

def auth_page(info=False):
    if request.method == "GET":
        if info == "#/SignUpSuccess":
            flash("Your account created successfully!","info")
        return render_template("auth.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        
        
        if username == "" or password == "":
            flash("You can not leave blank space.","error")
            return render_template("auth.html")
                
            #TODO return redirect(next or url_for("profile_page",username=username))
                  
        
        flash("Your Log In informations are incorrect","error")
        return render_template("auth.html")      

def account_create_page():
    form = CreateAccountForm()
    if form.validate_on_submit():
        username = form.data["username"]
        password = form.data["password"]
        
        return redirect(url_for("auth_page", info="#/SignUpSuccess"))

    return render_template("accountcreate.html",form=form)

def profile_page():
    global image
    global id
    form = ProfileUpdateForm()
    
    if form.validate_on_submit():
        
        if request.form["update"] == "Update Profile Information":
            return render_template("profile.html", form=form, update=True,profileimage=image)

        if request.form["update"] == "Save Changes":
            image_file = form.image.data
            
            if image_file != None:
                image = uploadImage(BytesIO(image_file.read()),id)
                print(image)
                id+=1
            
            return render_template("profile.html", form=form, update=False, profileimage=image)      
    
    return render_template("profile.html", update=False, form=form, profileimage=image)
    #TODO
    #username = request.args['username']
    #for user in users:
    #    if user.username == username:
    #        if username == logged_user:
    #            if request.method == "GET":
    #                return render_template("profile.html", username=username)
    #            else:
    #                return render_template("profile.html")
    
   
    
    