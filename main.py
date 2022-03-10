from flask import Flask, render_template, request, Response, send_file, make_response, send_from_directory
from storage_manager import StorageManager
from excel_writer import ExcelWriter

app = Flask(__name__)
s = StorageManager()

@app.route('/download', methods=['GET', 'POST'])
def download():    
    return send_from_directory(directory='/temp', filename="example.pdf")

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
        print("doing excel")
        excel = ExcelWriter(odberatel, dodavatel, [Item(dodavka, dph, count, price)], False, True, False, date, "", faktura_numbering, s) 
        #return render_template("index.html", status="Hotovo: "+excel.status)
        output = make_response(excel.invoice)
        output.headers["Content-Disposition"] = "attachment; filename=sheet.xlsx"
        output.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return output


    return render_template("index.html", status="")
