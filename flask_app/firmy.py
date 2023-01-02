from flask import render_template, request, session, redirect
from python.database_handler import *
from python.excel_handler import *
from python.user_handler import *
from main import app, login_required


@app.route("/add_firma", methods = ["GET", "POST"])
@login_required
def add_firma():
	firma = get_firma_dict(request.form)
	msg = "error"
	if firma and firma["name"]:
		msg = database_add_firma(session["user_data"], firma)
	return render_template("pridat_firmu.html", msg=msg, firmy=get_user_firmy_limit(session["user_data"], 0, 10))


@app.route("/change_firma", methods = ["GET", "POST"])
@login_required
def change_firma():
	delete_firma_by_id(session["user_data"], request.form.get("id"))
	firma = get_firma_dict(request.form)
	print(request.form.get("id"))
	print(firma)
	msg = "error"
	if firma and firma["name"]:
		msg = database_add_firma(session["user_data"], firma)
	return render_template("pridat_firmu.html", msg=msg, firmy=get_user_firmy_limit(session["user_data"], 0, 10))


@app.route("/smazat_firmu", methods = ["GET"])
@login_required
def smazat_firmu():
	delete_firma_by_id(session["user_data"], request.args.get("id"))
	return redirect("pridat_firmu", code=302)


@app.route("/pridat_firmu")
@login_required
def pridat_firmu():
	firmy = get_user_firmy_limit(session["user_data"], 0, 10)
	return render_template("pridat_firmu.html", firmy=firmy)


@app.route("/upravit_firmu")
@login_required
def upravit_firmu():
	firma_id = request.args.get("id")
	firma = get_firma_data_from_id(session["user_data"], firma_id)
	firmy = get_user_firmy_limit(session["user_data"], 0, 10)
	print(firma)
	return render_template("pridat_firmu.html", firmy=firmy, firma=firma, firma_id=firma_id)