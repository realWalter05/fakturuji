from flask import render_template, request, make_response, session, Response, redirect
import pdfkit, json
from python.database_handler import *
from python.excel_handler import *
from python.user_handler import *
from main import app, login_required, index


@app.route('/get_ucetnictvi_in_date')
@login_required
def get_ucetnictvi():
	ucetnictvi_od = request.args.get('ucetnictvi_od')
	ucetnictvi_do = request.args.get('ucetnictvi_do')

	faktury = get_faktury_by_user(session["user_data"])
	if not faktury:
		return index()
	polozky = get_polozky_by_faktura_id(session["user_data"], faktury)

	excel = get_all_faktury_in_date(session["user_data"], faktury, polozky, ucetnictvi_od, ucetnictvi_do)
	output = make_response(excel.get_virtual_save())
	output.headers["Content-Disposition"] = f"attachment; filename=ucetnictvi.xlsx"
	output.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
	return output


@app.route('/get_faktura')
@login_required
def get_faktura():
	faktura_id = request.args.get('id')
	faktury = get_faktury_by_id(session["user_data"], faktura_id)
	polozky = get_polozky_by_faktura_id(session["user_data"], faktury)

	excel = get_all_faktury(session["user_data"], faktury, polozky)
	output = make_response(excel.get_virtual_save())
	output.headers["Content-Disposition"] = f"attachment; filename=sheet{excel.faktura_numbering}.xlsx"
	output.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
	return output


@app.route("/get_faktura_html", methods = ["GET", "POST"])
@login_required
def get_faktura_html():
	faktura_id = request.args.get('id')
	return get_faktura_template(session["user_data"], faktura_id)


@app.route('/get_faktura_pdf')
@login_required
def get_faktura_pdf():
	path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
	config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
	options = {'disable-smart-shrinking': ''}

	faktura_id = request.args.get('id')
	rendered = get_faktura_template(session["user_data"], faktura_id)
	pdf = pdfkit.from_string(rendered, options=options, configuration=config)
	return Response(pdf, mimetype="application/pdf",headers={"Content-Disposition":"attachment;filename=faktura.pdf"})


@app.route("/upravit_fakturu", methods = ["GET", "POST"])
@login_required
def upravit_fakturu():
	faktura_id = request.args.get('id')

	faktura_data = get_faktura_by_id(session["user_data"], faktura_id)
	dodavatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["dodavatel"])
	odberatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["odberatel"])
	polozky = get_polozky_by_faktura_id(session["user_data"], faktura_data)[0]

	popisek = None
	if faktura_data[0]["description_id"] != "":
		popisek_list = get_popisek_by_id(session["user_data"], faktura_data[0]["description_id"])
		if popisek_list:
			popisek = popisek_list[0]

	return render_template("upravit_fakturu.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky, popisek=popisek)


@app.route("/faktury")
@login_required
def faktury():
	faktury = get_user_full_faktury(get_user_faktury_limit(session["user_data"], 0, 10), session["user_data"])
	return render_template("faktury.html", faktury=faktury)


@app.route("/process_faktura", methods = ["GET", "POST"])
@login_required
def process_faktura():
	# Getting the form data
	post_faktura(session["user_data"], request.args)
	return redirect("/", code=302)

@app.route("/process_jednorazova_faktura", methods = ["GET", "POST"])
def process_jednorazova_faktura():
	excel = create_jednorazova_faktura_excel(request.args)
	output = make_response(excel.get_virtual_save())
	output.headers["Content-Disposition"] = f"attachment; filename=sheet{excel.faktura_numbering}.xlsx"
	output.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
	return output


@app.route("/process_upravit_fakturu", methods = ["GET", "POST"])
@login_required
def process_upravit_fakturu():
	# Getting the form data
	delete_whole_faktura_by_id(session["user_data"], request.args.get("faktura_id"))
	post_faktura(session["user_data"], request.args)
	return redirect("faktury", code=302)


@app.route("/get_dalsi_faktury", methods = ["GET"])
@login_required
def get_dalsi_faktury():
	from_faktury = request.args.get("from")
	to_faktury = request.args.get("to")

	faktury = get_user_full_faktury(get_user_faktury_limit(session["user_data"], from_faktury, to_faktury), session["user_data"])
	return json.dumps(faktury, indent=4, sort_keys=True, default=str)


@app.route("/smazat_fakturu", methods = ["GET"])
@login_required
def smazat_fakturu():
	# Getting the form data
	delete_whole_faktura_by_id(session["user_data"], request.args.get("id"))
	return redirect("faktury", code=302)


@app.route("/fakturujto_jednou")
def fakturujto_jednou():
	return render_template("fakturujto_jednou.html")


@app.route("/fakturujto")
@login_required
def fakturujto():
	return render_template("fakturujto.html")