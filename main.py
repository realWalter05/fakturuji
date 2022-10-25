from flask import Flask, render_template, request, send_file, make_response, session, send_file, abort
from excel_writer_old import ExcelWriter
from excel_handler import *
from database_handler import *
from user_handler import *
import os, io, secrets, json, requests

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



@app.route('/get_user_firmy_names', methods=['GET', 'POST'])
@login_required
def get_firmy():
    search_text = request.args.get('search_text')
    je_dodavatel = request.args.get('je_dodavatel')
    je_odberatel = request.args.get('je_odberatel')    
    names = get_user_firmy_names(session["user_data"], search_text, je_dodavatel, je_odberatel)
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


@app.route("/")
def index():
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
    faktury = get_user_faktury(session["user_data"])
    print(faktury)
    return render_template("settings.html", faktury=faktury)


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
    if firma and firma["name"] and session["user_data"]:
        msg = database_add_firma(session["user_data"], firma)
    return render_template("settings.html", msg=msg)  



@app.route("/faktura", methods = ["GET", "POST"])
def faktura():
    # Getting the form data
    date = {
        "vystaveni_date": request.args.get("splatnost_date"),
        "zdanpl_date": request.args.get("zdanpl_date"),
        "splatnost_date": request.args.get("vystaveni_date"),
    }
    
    items = get_user_items(request.args)
    dodavatel_list = get_dodavatel_list(request.args)
    odberatel_list = get_odberatel_list(request.args)

    faktura_numbering = request.args.get("faktura_numbering")
    prenesena_dph = request.args.get("prenesena_dph")
    dodavatel_dph = request.args.get("dodavatel_dph")
    qr_platba = request.args.get("qr_platba")
    vystavila_osoba = request.args.get("vystavila_osoba")

    # Faktura in PDF with unique string
    excel = ExcelWriter()
    excel.create_faktura(dodavatel_list, odberatel_list, items, 1 if prenesena_dph == 1 else 0, dodavatel_dph, qr_platba, date, "", faktura_numbering, vystavila_osoba) 
    output = make_response(excel.get_virtual_save())
    output.headers["Content-Disposition"] = f"attachment; filename=ucetnictvi.xlsx"
    output.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return output  


@app.route("/process_faktura", methods = ["GET", "POST"])
@login_required
def process_faktura():
    # Getting the form data
    post_faktura(session["user_data"], request.args)
    return render_template("index.html")  


