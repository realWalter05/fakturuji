from flask import render_template, request, session, redirect
import json
from python.database_handler import *
from python.excel_handler import *
from python.user_handler import *
from main import app, login_required


@app.route("/popisky")
@login_required
def popisky():
	popisky = get_user_popisky_limit(session["user_data"], 0, 10)
	return render_template("popisky.html", popisky=popisky)


@app.route("/add_popisek", methods = ["GET", "POST"])
@login_required
def add_popisek():
	popisek = {
		"nazev" : request.args.get("nazev"),
		"popisek" : request.args.get("popisek"),
		"je_sifrovano" : 1 if request.args.get("je_sifrovano") == "on" else 0
	}
	msg = "error"
	if popisek["nazev"]:
		msg = database_add_popisek(session["user_data"], popisek)

	return redirect("popisky", code=302)


@app.route("/edit_popisek", methods = ["GET", "POST"])
@login_required
def edit_popisek():
	popisek = {
		"nazev" : request.args.get("nazev"),
		"popisek" : request.args.get("popisek"),
		"je_sifrovano" : 1 if request.args.get("je_sifrovano") == "on" else 0
	}

	delete_popisek_by_id(session["user_data"], request.args.get("id"))
	if popisek["nazev"]:
		database_add_popisek(session["user_data"], popisek)

	return redirect("popisky", code=302)


@app.route("/get_dalsi_popisky", methods = ["GET"])
@login_required
def get_dalsi_popisky():
	from_popisky = request.args.get("from")
	to_popisky = request.args.get("to")

	popisky = get_user_popisky_limit(session["user_data"], from_popisky, to_popisky)
	return json.dumps(popisky, indent=4, sort_keys=True, default=str)


@app.route("/smazat_popisek", methods = ["GET"])
@login_required
def smazat_popisek():
	# Getting the form data
	delete_popisek_by_id(session["user_data"], request.args.get("id"))
	return redirect("popisky", code=302)