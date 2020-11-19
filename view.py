from flask import Flask, render_template, request, redirect, url_for, flash
from objects.person import *
from tools.hash import hash_password

def auth_page(popup=False,msg=None):
    if request.method == "GET":
        return render_template("auth.html")
    else:
        name = request.form.get("username")
        print(name)
        return render_template("auth.html",popup=popup,msg=msg)


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
            return redirect(url_for("account_create_page"))

        password = hash_password(password)

        person = Person(username,id_number,password,mail,account_type,faculty)
        person.debug_person()
        return auth_page(popup=True, msg="Your Account succesfully created!!")
