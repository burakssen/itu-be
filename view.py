from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, current_app
from tools.hash import hash_password, hash_control
from flask_login import login_user, login_required
from forms import CreateAccountForm

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
    return render_template("profile.html",username="burak")
    #TODO
    #username = request.args['username']
    #for user in users:
    #    if user.username == username:
    #        if username == logged_user:
    #            if request.method == "GET":
    #                return render_template("profile.html", username=username)
    #            else:
    #                return render_template("profile.html")
    
   
    
    