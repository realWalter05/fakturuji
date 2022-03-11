from flask import Flask, render_template, request, Response, send_file, make_response, send_from_directory
from storage_manager import StorageManager
from excel_writer import ExcelWriter
import os

app = Flask(__name__)
s = StorageManager()

@app.route('/download', methods=['GET', 'POST'])
def download():    
    return send_from_directory(app.root_path, "faktura.pdf", as_attachment=True)

@app.route("/", methods = ["GET", "POST"])
def index():
    class Item():
        def __init__(self, dodavka, dph, count, price):
            self.delivery_name = dodavka
            self.dph = dph
            self.count = count
            self.price = price

    date = {
        "vystaveni_date": request.args.get("splatnost_date"),
        "zdanpl_date": request.args.get("zdanpl_date"),
        "splatnost_date": request.args.get("vystaveni_date"),
    }


    dodavatel = request.args.get("dodavatel")
    odberatel = request.args.get("odberatel")
    faktura_numbering = request.args.get("faktura_numbering")
    dodavka = request.args.get("dodavka")
    dph = request.args.get("dph")
    count = request.args.get("count")
    price = request.args.get("price")

    prenesena_dph = request.args.get("prenesena_dph")
    dodavatel_dph = request.args.get("dodavatel_dph")
    qr_platba = request.args.get("qr_platba")
    pdf = request.args.get("pdf")

    print(dodavatel, odberatel)
    print(prenesena_dph, dodavatel_dph, qr_platba, pdf)

    if dodavatel:
        excel = ExcelWriter(odberatel, dodavatel, [Item(dodavka, dph, count, price)], prenesena_dph, dodavatel_dph, qr_platba, date, "", faktura_numbering, s, pdf) 
        output = make_response(excel.invoice)
        output.headers["Content-Disposition"] = "attachment; filename=sheet.xlsx"
        output.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return output


    return render_template("index.html", status="")
