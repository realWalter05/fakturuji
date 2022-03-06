from flask import Flask, render_template, request, Response, send_file, make_response
from storage_manager import StorageManager
from excel_writer import ExcelWriter

app = Flask(__name__)
s = StorageManager()

@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    excel = ""
    output = excel.make_response()
    output.headers["Content-Disposition"] = "attachment; filename=sheet.xlsx"
    output.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return output

@app.route("/", methods = ["GET", "POST"])
def index():
    print("here")

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

    print(dodavatel, odberatel)

    if dodavatel:
        excel = ExcelWriter(odberatel, dodavatel, [Item(dodavka, dph, count, price)], True, True, False, date, "", faktura_numbering, s) 
        #return render_template("index.html", status="Hotovo: "+excel.status)
        output = make_response(excel.invoice)
        output.headers["Content-Disposition"] = "attachment; filename=sheet.xlsx"
        output.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return output

    print("nope")

    return render_template("index.html", status="")
