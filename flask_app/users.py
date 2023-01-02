from flask import render_template, request, session, redirect
from python.database_handler import *
from python.excel_handler import *
from python.user_handler import *
from main import app, login_required, index


@app.route("/account")
@login_required
def account():
	return render_template("account.html")


@app.route("/unlogin")
@login_required
def unlogin():
	session.pop("user_data", None)
	return render_template("index.html")


@app.route("/register")
def register():
	return render_template("register.html")


@app.route("/login")
def login():
	return render_template("login.html")


@app.route("/register_user", methods = ["GET", "POST"])
def register_username():
	msg = register_user(request.form["username"], request.form["email"], request.form["password"], request.form["password-repeat"])
	if msg == "success":
		return login_username()
	return render_template("register.html", msg=msg)


@app.route("/login_user", methods = ["GET", "POST"])
def login_username():
	msg = login_user(request.form["username"], request.form["password"])

	if isinstance(msg, tuple):
		# If it is tuple it was success
		session["user_data"] = {
			"id": msg[0],
			"name": msg[1],
			"email": msg[2],
			"data_key": decrypt_data(request.form["password"], msg[4])
		}
		msg = "success"
		return index()

	return render_template("login.html", msg=msg)


@app.route("/delete_everything")
@login_required
def delete_everything():
	faktury = get_user_faktury(session["user_data"])
	for faktura in faktury:
		delete_whole_faktura_by_id(session["user_data"], faktura["id"])

	sablony = get_user_sablony(session["user_data"])
	for sablona in sablony:
		delete_sablona_by_id(session["user_data"], sablona["sid"])

	popisky = get_user_popisky(session["user_data"])
	for popisek in popisky:
		delete_popisek_by_id(session["user_data"], popisek["id"])

	firmy = get_user_firmy(session["user_data"])
	for firma in firmy:
		delete_firma_by_id(session["user_data"], firma["id"])

	delete_user_account(session["user_data"], session["user_data"]["id"])
	session.clear()
	return redirect("/", code=302)