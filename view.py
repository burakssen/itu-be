from flask import Flask, render_template, request, redirect, url_for, flash, json, session
from objects.person import *
from tools.hash import hash_password, hash_control

persons = []

def auth_page(info=False):
    if request.method == "GET":
        if info == "info":
            flash("Your account created successfully!","info")
        return render_template("auth.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        
        for person in persons:
            if person.username == username:
                if hash_control(password, person.password):
                    return redirect(url_for("profile_page",username=username))
                else:
                    return render_template("auth.html")
            else:
                return render_template("auth.html")      
        
        return render_template("auth.html")  


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
            flash("You can't leave any blank spaces","error");
            return redirect(url_for("account_create_page"))

        password = hash_password(password)

        person = Person(username,id_number,password,mail,account_type,faculty)
        persons.append(person)
        
        return redirect(url_for("auth_page",info="info"))

def profile_page():
    username = request.args['username']
    if request.method == "GET":
        return render_template("profile.html", username=username)
    else:
        return render_template("profile.html", username=username)