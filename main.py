from dateutil.relativedelta import relativedelta
import json
from flask import Flask, render_template, request, session


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")


from python.database_handler import *
from python.excel_handler import *
from python.user_handler import *



# Index
@app.route("/")
def index():
	print(app.config)
	if "user_data" in session:
		faktury = get_user_full_faktury(get_user_faktury_limit(session["user_data"], 0, 3), session["user_data"])
		if not faktury:
			return render_template("login.html", msg="database_timeout")

		sablony = get_user_sablony_limit(session["user_data"], 0, 4)
		get_ucetnictvi_data = {"from" : (datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d"), "to" : datetime.today().strftime("%Y-%m-%d")}
		return render_template("prehled.html", faktury=faktury, sablony=sablony, get_ucetnictvi_data=get_ucetnictvi_data)

	return render_template("index.html")

# Decorators
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

# JSON
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

	unfiltered = names = get_user_firmy_names(session["user_data"], je_dodavatel, je_odberatel)
	if search_text.strip() != "":
		# If search text is not empty, filter result
		names = filter_user_firmy(unfiltered, search_text)

		if len(names) == 1:
			if names[0]["nazev"] == search_text:
				return json.dumps(unfiltered)

		return json.dumps(names)

	return json.dumps(unfiltered)


@app.route("/get_dalsi_firmy", methods = ["GET"])
@login_required
def get_dalsi_firmy():
	from_firmy = request.args.get("from")
	to_firmy = request.args.get("to")

	firmy = get_user_firmy_limit(session["user_data"], from_firmy, to_firmy)
	return json.dumps(firmy, indent=4, sort_keys=True, default=str)

# Import other parts of app
import flask_app.faktury, flask_app.sablony, flask_app.popisky, flask_app.firmy, flask_app.users