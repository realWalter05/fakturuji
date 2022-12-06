from flask import Flask, render_template, request, send_file, make_response, session, send_file, Response
import pdfkit
from excel_writer import ExcelWriter
from excel_handler import *
from database_handler import *
from user_handler import *
import json
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "I\x99\x1a\x88o\x95\xcdIr\xbe\xed\xa8\xbav\x82G1\x98\x17\xb5\x7f\rJ~"


def login_required(func):
	def wrapper():
		print("Checking login")
		if "user_data" not in session:
			print("User is not logged")
			return render_template("login.html", msg="login_required")

		if "id" not in session["user_data"]:
			print("User is not logged")
			return render_template("login.html", msg="login_required")

		print("User is logged")
		return func()
	wrapper.__name__ = func.__name__
	return wrapper


@app.route('/get_ico_data', methods=['GET', 'POST'])
def get_ico_data():
	text = request.args.get('jsdata')
	return json.dumps(auto_fill(text, ""))


@app.route('/get_data_from_id', methods=['GET', 'POST'])
@login_required
def get_data_from_id():
	id = request.args.get('id')
	data = get_firma_data_from_id(session["user_data"], id)
	return json.dumps(data)


@app.route('/get_popisky', methods=['GET', 'POST'])
@login_required
def get_popisky():
	search_text = request.args.get('search_text')
	names = get_database_popisky(session["user_data"], search_text)
	return json.dumps(names)


@app.route('/get_user_firmy_names', methods=['GET', 'POST'])
@login_required
def get_firmy():
	search_text = request.args.get('search_text')
	je_dodavatel = request.args.get('je_dodavatel')
	je_odberatel = request.args.get('je_odberatel')

	names = get_user_firmy_names(session["user_data"], je_dodavatel, je_odberatel)
	if search_text.strip() != "":
		# If search text is not empty, filter result
		names = filter_user_firmy(names, search_text)
		print(f"filtered {names}")

	return json.dumps(names)


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
	faktura_data = get_faktura_by_id(session["user_data"], faktura_id)
	dodavatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["dodavatel"])
	odberatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["odberatel"])
	polozky = get_polozky_by_faktura_id(session["user_data"], faktura_data)[0]
	polozky = get_prices_polozky(polozky)

	faktura_data[0]["total_bez_dph"] = 0
	faktura_data[0]["total_s_dph"] = 0
	for polozka in polozky:
		faktura_data[0]["total_bez_dph"] += polozka["bez_dph"]
		faktura_data[0]["total_s_dph"] += polozka["s_dph"]

	faktura_data[0]["datum_vystaveni"] = faktura_data[0]["datum_vystaveni"].strftime("%d.%m.%Y")
	faktura_data[0]["datum_zdanpl"] = faktura_data[0]["datum_zdanpl"].strftime("%d.%m.%Y")
	faktura_data[0]["datum_splatnosti"] = faktura_data[0]["datum_splatnosti"].strftime("%d.%m.%Y")

	if faktura_data[0]["qr_platba"]:
		# qr platba
		"data:image/jpeg;base64,"
		buffered = BytesIO()
		response = requests.get("https://api.paylibo.com/paylibo/generator/czech/image?accountNumber="+str(int(dodavatel[13]))+
                        "&bankCode="+str(int(dodavatel[14]))+"&amount="+str(faktura_data[0]["total_s_dph"])+"&currency=CZK&vs="+str(dodavatel[17])+"&size=200")
		image = Image.open(BytesIO(response.content))
		image.save(buffered, format="JPEG")
		img_str = base64.b64encode(buffered.getvalue())
		base_image = img_str.decode("utf-8")
		return render_template("faktura_template_qr.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky, qr_platba_base=base_image)

	return render_template("faktura_template.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky)



@app.route('/get_faktura_pdf')
@login_required
def get_faktura_pdf():
	path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
	config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
	options = {'disable-smart-shrinking': ''}

	faktura_id = request.args.get('id')
	faktura_data = get_faktura_by_id(session["user_data"], faktura_id)
	dodavatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["dodavatel"])
	odberatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["odberatel"])
	polozky = get_polozky_by_faktura_id(session["user_data"], faktura_data)[0]
	polozky = get_prices_polozky(polozky)

	faktura_data[0]["total_bez_dph"] = 0
	faktura_data[0]["total_s_dph"] = 0
	for polozka in polozky:
		faktura_data[0]["total_bez_dph"] += polozka["bez_dph"]
		faktura_data[0]["total_s_dph"] += polozka["s_dph"]

	faktura_data[0]["datum_vystaveni"] = faktura_data[0]["datum_vystaveni"].strftime("%d.%m.%Y")
	faktura_data[0]["datum_zdanpl"] = faktura_data[0]["datum_zdanpl"].strftime("%d.%m.%Y")
	faktura_data[0]["datum_splatnosti"] = faktura_data[0]["datum_splatnosti"].strftime("%d.%m.%Y")

	if faktura_data[0]["qr_platba"]:
		# qr platba
		"data:image/jpeg;base64,"
		buffered = BytesIO()
		response = requests.get("https://api.paylibo.com/paylibo/generator/czech/image?accountNumber="+str(int(dodavatel[13]))+
                        "&bankCode="+str(int(dodavatel[14]))+"&amount="+str(faktura_data[0]["total_s_dph"])+"&currency=CZK&vs="+str(dodavatel[17])+"&size=200")
		image = Image.open(BytesIO(response.content))
		image.save(buffered, format="JPEG")
		img_str = base64.b64encode(buffered.getvalue())
		base_image = img_str.decode("utf-8")
		return render_template("faktura_template_qr.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky, qr_platba_base=base_image)

	print(f"{faktura_data[0]} polozky")
	rendered = render_template("faktura_template.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky)
	pdf = pdfkit.from_string(rendered, options=options, configuration=config)
	return Response(pdf, mimetype="application/pdf",headers={"Content-Disposition":"attachment;filename=faktura.pdf"})


@app.route("/")
def index():
	if "user_data" in session:
		faktury = get_user_full_faktury(get_user_faktury_limit(session["user_data"], 0, 3), session["user_data"])
		sablony = get_user_sablony_limit(session["user_data"], 0, 4)
		return render_template("prehled.html", faktury=faktury, sablony=sablony)

	return render_template("index.html")


@app.route("/upravit_fakturu", methods = ["GET", "POST"])
@login_required
def upravit_fakturu():
	faktura_id = request.args.get('id')

	faktura_data = get_faktura_by_id(session["user_data"], faktura_id)
	dodavatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["dodavatel"])
	odberatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["odberatel"])
	polozky = get_polozky_by_faktura_id(session["user_data"], faktura_data)[0]

	return render_template("upravit_fakturu.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky)



@app.route("/fakturuj_sablonu", methods = ["GET", "POST"])
@login_required
def fakturuj_sablonu():
	faktura_id = request.args.get('id')

	faktura_data = get_faktura_by_id(session["user_data"], faktura_id)
	dodavatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["dodavatel"])
	odberatel = get_firma_data_from_id(session["user_data"], faktura_data[0]["odberatel"])
	polozky = get_polozky_by_faktura_id(session["user_data"], faktura_data)[0]

	return render_template("fakturujto.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky)



@app.route("/fakturujto")
@login_required
def fakturujto():
	return render_template("fakturujto.html")


@app.route("/sablony")
@login_required
def sablony():
	faktury = get_user_full_sablony(get_user_sablony_limit(session["user_data"], 0, 10), session["user_data"])
	return render_template("sablony.html", sablony=faktury)


@app.route("/faktury")
@login_required
def faktury():
	faktury = get_user_full_faktury(get_user_faktury_limit(session["user_data"], 0, 10), session["user_data"])
	return render_template("faktury.html", faktury=faktury)


@app.route("/fakturujto_jednou")
def fakturujto_jednou():
	return render_template("fakturujto_jednou.html")


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
	return render_template("pridat_firmu.html", firmy=firmy, firma=firma, firma_id=firma_id)


@app.route("/popisky")
@login_required
def popisky():
	popisky = get_user_popisky(session["user_data"], )
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

	return render_template("popisky.html", msg=msg)


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


@app.route("/add_firma", methods = ["GET", "POST"])
@login_required
def add_firma():
	firma = get_firma_dict(request.args)
	msg = "error"
	if firma and firma["name"]:
		msg = database_add_firma(session["user_data"], firma)
	return render_template("pridat_firmu.html", msg=msg, firmy=get_user_firmy_limit(session["user_data"], 0, 10))


@app.route("/change_firma", methods = ["GET", "POST"])
@login_required
def change_firma():
	delete_firma_by_id(session["user_data"], request.args.get("id"))
	firma = get_firma_dict(request.args)
	msg = "error"
	if firma and firma["name"]:
		msg = database_add_firma(session["user_data"], firma)
	return render_template("pridat_firmu.html", msg=msg, firmy=get_user_firmy_limit(session["user_data"], 0, 10))


@app.route("/smazat_firmu", methods = ["GET", "POST"])
@login_required
def smazat_firmu():
	delete_firma_by_id(session["user_data"], request.args.get("id"))
	return render_template("pridat_firmu.html", firmy=get_user_firmy_limit(session["user_data"], 0, 10))


@app.route("/process_faktura", methods = ["GET", "POST"])
@login_required
def process_faktura():
	# Getting the form data
	post_faktura(session["user_data"], request.args)
	return index()


@app.route("/process_upravit_fakturu", methods = ["GET", "POST"])
@login_required
def process_upravit_fakturu():
	# Getting the form data
	delete_whole_faktura_by_id(session["user_data"], request.args.get("faktura_id"))
	post_faktura(session["user_data"], request.args)
	return render_template("index.html")


@app.route("/z_faktury_sablonu", methods = ["GET"])
@login_required
def z_faktury_sablonu():
	make_sablona_from_id(session["user_data"], request.args.get("id"))
	return sablony()


@app.route("/get_dalsi_faktury", methods = ["GET"])
@login_required
def get_dalsi_faktury():
	from_faktury = request.args.get("from")
	to_faktury = request.args.get("to")

	faktury = get_user_full_faktury(get_user_faktury_limit(session["user_data"], from_faktury, to_faktury), session["user_data"])
	return json.dumps(faktury, indent=4, sort_keys=True, default=str)


@app.route("/get_dalsi_sablony", methods = ["GET"])
@login_required
def get_dalsi_sablony():
	from_sablony = request.args.get("from")
	to_sablony = request.args.get("to")

	faktury = get_user_full_sablony(get_user_sablony_limit(session["user_data"], from_sablony, to_sablony), session["user_data"])
	print(faktury, from_sablony, to_sablony)
	print(get_user_sablony_limit(session["user_data"], from_sablony, to_sablony))
	return json.dumps(faktury, indent=4, sort_keys=True, default=str)


@app.route("/smazat_fakturu", methods = ["GET"])
@login_required
def smazat_fakturu():
	# Getting the form data
	delete_whole_faktura_by_id(session["user_data"], request.args.get("id"))
	return faktury()

@app.route("/smazat_sablonu", methods = ["GET", "POST"])
@login_required
def smazat_sablonu():
	# Getting the form data
	delete_sablona_by_id(session["user_data"], request.args.get("id"))
	return sablony()


@app.route("/smazat_popisek", methods = ["GET", "POST"])
@login_required
def smazat_popisek():
	# Getting the form data
	print(request.args.get("id"))
	delete_popisek_by_id(session["user_data"], request.args.get("id"))
	popisky = get_user_popisky(session["user_data"], )
	return render_template("popisky.html", popisky=popisky)


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
	return index()
