from flask import Flask, render_template, request

def auth_page():
    if request.method == "GET":
        return render_template("auth.html")
    else:
        name = request.form.get("username")
        print(name)
        return render_template("auth.html")


def account_create_page():
    if request.method == "GET":
        return render_template("accountcreate.html")
    else:
        name = request.form.get("accounttype")
        print(name)
        return render_template("accountcreate.html")
