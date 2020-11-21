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

"""
def account_create_page():
    if request.method == "GET":
        return render_template("accountcreate.html")
    else:
        username = request.form.get("username")
        id_number = request.form.get("id-number")
        password = request.form.get("password")
        mail = request.form.get("mail")
        account_type = request.form.get("accounttype")
        faculty = request.form.get("faculty")

        if username == "" or id_number == "" or password == "" or mail == "" or account_type == "" or faculty == "":
            flash("You can't leave any blank spaces","error")
            return redirect(url_for("account_create_page"))

        password = hash_password(password)

        #TODO user = User(username,id_number,password,mail,account_type,faculty)
        #current_app.config['PASSWORDS'] = [username, password]
        #users.append(user)
        
        return redirect(url_for("auth_page",info="info"))
"""

def account_create_page():
    form = CreateAccountForm()
    if form.validate_on_submit():
        username = form.data["username"]
        password = form.data["password"]
        
        return redirect(url_for("auth_page", info="#/SignUpSuccess"))

    return render_template("accountcreate.html",form=form)


def profile_page():
    pass
    #TODO
    #username = request.args['username']
    #for user in users:
    #    if user.username == username:
    #        if username == logged_user:
    #            if request.method == "GET":
    #                return render_template("profile.html", username=username)
    #            else:
    #                return render_template("profile.html")
    
    #return render_template("auth.html")
    
    