from flask import Flask, render_template, request, send_file, make_response, session, send_file, abort, Response, render_template_string
from excel_writer import ExcelWriter
from excel_handler import *
from database_handler import *
from user_handler import *
import json

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
	print(names)
	if search_text.strip() != "":
		# If search text is not empty, filter result
		names = filter_user_firmy(names, search_text)
		print(f"filtered {names}")

	return json.dumps(names)


@app.route('/get_ucetnictvi')
@login_required
def get_ucetnictvi():
	faktury = get_faktury_by_user(session["user_data"])
	polozky = get_polozky_by_faktura_id(session["user_data"], faktury)

	excel = get_all_faktury(session["user_data"], faktury, polozky)
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


@app.route("/print_faktura")
@login_required
def print_faktura(): 	
	faktura_id = request.args.get('id')
	dodavatel = get_firma_data_from_id(session["user_data"], faktura_id)
	odberatel = get_firma_data_from_id(session["user_data"], faktura_id)
	return render_template("faktura_templatee.html", dodavatel=dodavatel, odberatel=odberatel)	


@app.route('/get_faktura_pdf')
@login_required
def get_faktura_pdf():
	import pdfkit
	path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
	config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
	options = {
	    'page-height': '210mm', 
	    'page-width': '148mm',
	}

	resp = Response(pdfkit.from_file('./templates/faktura_templatee.html', options=options, configuration=config), mimetype="application/pdf",
					headers={"Content-Disposition":"attachment;filename=outfile.pdf"})	
	print(render_template_string('./templates/faktura_templatee.html'))
	return resp


@app.route("/")
def index():
	if "user_data" in session:
		faktury = get_user_faktury(session["user_data"])[0:3]
		for faktura in faktury:
			dodavatel_id = int(faktura["dodavatel"])
			odberatel_id = int(faktura["odberatel"])
			faktura["dodavatel"] = get_firma_data_from_id(session["user_data"], dodavatel_id)[0]
			faktura["odberatel"] = get_firma_data_from_id(session["user_data"], odberatel_id)[0]
		return render_template("prehled.html", faktury=faktury)
	return render_template("index.html")
	


@app.route("/fakturujto")
@login_required
def fakturujto():
	return render_template("fakturujto.html")


@app.route("/fakturujto_jednou")
def fakturujto_jednou(): 	
	return render_template("fakturujto_jednou.html")



@app.route("/settings")
@login_required
def settings():
	return render_template("settings.html")


@app.route("/pridat_firmu")
@login_required
def pridat_firmu():
	return render_template("pridat_firmu.html")


@app.route("/upravit_firmu")
@login_required
def upravit_firmu():
	firmy = get_user_firmy(session["user_data"])
	print(firmy)
	return render_template("upravit_firmu.html", firmy=firmy)


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
	count = len(get_user_faktury(session["user_data"]))
	print(count)
	return render_template("account.html", faktura_count=count)


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
	msg = register_user(request.form["username"], request.form["password"])
	return render_template("register.html", msg=msg)


@app.route("/login_user", methods = ["GET", "POST"])
def login_username():
	msg = login_user(request.form["username"], request.form["password"])

	if isinstance(msg, tuple):
		# If it is tuple it was success
		session["user_data"] = {
			"id": msg[0],
			"name": msg[1],
			"data_key": decrypt_data(request.form["password"], msg[3])
		}
		msg = "success"

	return render_template("login.html", msg=msg)  


@app.route("/add_firma", methods = ["GET", "POST"])
@login_required
def add_firma():
	firma = get_firma_dict(request.args)
	msg = "error"
	if firma and firma["name"]:
		msg = database_add_firma(session["user_data"], firma)
	return render_template("settings.html", msg=msg)  


@app.route("/process_faktura", methods = ["GET", "POST"])
@login_required
def process_faktura():
	# Getting the form data
	post_faktura(session["user_data"], request.args)
	return render_template("index.html")  
