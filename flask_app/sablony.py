from flask import render_template, request, session, redirect
import json
from python.database_handler import *
from python.excel_handler import *
from python.user_handler import *
from main import app, login_required


@app.route("/sablony")
@login_required
def sablony():
	faktury = get_user_full_sablony(get_user_sablony_limit(session["user_data"], 0, 10), session["user_data"])
	return render_template("sablony.html", sablony=faktury)


@app.route("/z_faktury_sablonu", methods = ["GET"])
@login_required
def z_faktury_sablonu():
	make_sablona_from_copy_id(session["user_data"], request.args.get("id"), request.args.get("sablona_name"))
	return redirect("sablony", code=302)


@app.route("/upravit_sablonu", methods = ["GET", "POST"])
@login_required
def upravit_sablonu():
	faktura_id = request.args.get('id')

	faktura_data = get_faktura_by_id(session["user_data"], faktura_id)
	dodavatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["dodavatel"])
	odberatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["odberatel"])
	polozky = get_polozky_by_faktura_id(session["user_data"], faktura_data)[0]

	sablona_sid = request.args.get('sid')
	sablona_name = get_sablona_by_id(session["user_data"], sablona_sid)[0]["nazev"]

	popisek = None
	if faktura_data[0]["description_id"] != "":
		popisek_list = get_popisek_by_id(session["user_data"], faktura_data[0]["description_id"])
		if popisek_list:
			popisek = popisek_list[0]

	return render_template("upravit_fakturu.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky, sablona_sid=sablona_sid, sablona_name=sablona_name, popisek=popisek)



@app.route("/fakturuj_sablonu", methods = ["GET", "POST"])
@login_required
def fakturuj_sablonu():
	faktura_id = request.args.get('id')

	faktura_data = get_faktura_by_id(session["user_data"], faktura_id)
	dodavatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["dodavatel"])
	odberatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["odberatel"])
	polozky = get_polozky_by_faktura_id(session["user_data"], faktura_data)[0]

	return render_template("fakturujto.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky)


@app.route("/get_dalsi_sablony", methods = ["GET"])
@login_required
def get_dalsi_sablony():
	from_sablony = request.args.get("from")
	to_sablony = request.args.get("to")

	faktury = get_user_full_sablony(get_user_sablony_limit(session["user_data"], from_sablony, to_sablony), session["user_data"])
	print(faktury, from_sablony, to_sablony)
	print(get_user_sablony_limit(session["user_data"], from_sablony, to_sablony))
	return json.dumps(faktury, indent=4, sort_keys=True, default=str)


@app.route("/smazat_sablonu", methods = ["GET"])
@login_required
def smazat_sablonu():
	# Getting the form data
	delete_sablona_by_id(session["user_data"], request.args.get("id"))
	delete_faktura_by_id(session["user_data"], request.args.get("id"))
	return redirect("sablony", code=302)


@app.route("/process_upravit_sablonu", methods = ["GET"])
@login_required
def process_upravit_sablonu():
	# Getting the form data
	delete_faktura_by_id(session["user_data"], request.args.get("faktura_id"))
	delete_sablona_by_id(session["user_data"], request.args.get("sablona_sid"))
	post_sablona_faktura(session["user_data"], request.args)
	return redirect("sablony", code=302)