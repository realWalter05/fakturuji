from flask import Flask, render_template, request, Response, send_file, make_response, send_from_directory
from storage_manager import StorageManager
from excel_writer import ExcelWriter
import os

import json
import pandas as pd
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

def auto_fill(user_input, title):
   # Request to ares
   if user_input:
       user_ico = ""
       if user_input.replace(" ", "").isnumeric():
           user_ico = user_input.replace(" ", "")
       else:
           # If input is obchodni firma get its ico
           firma_url = "https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi?obchodni_firma=" + user_input
           try:
               xml_data = requests.get(firma_url)
               response = ET.fromstring(xml_data.content)
               firma_path = "{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1}"
               zaznam = response[0].find(firma_path + "Zaznam")
               if zaznam:
                   ico = zaznam.find(firma_path + "ICO")
                   user_ico = ico.text

           except requests.exceptions.ConnectionError:
               print("no internet")

       url = "http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_bas.cgi?ico=" + user_ico + "&adr_puv=true"
       try:
           xml_data = requests.get(url)

           odpoved = ET.fromstring(xml_data.content)

           path = "{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.3}"
           # Getting the data
           vbas = odpoved[0].find(path + "VBAS")
           if vbas:
               name = vbas.find(path + "OF").text if vbas.find(path + "OF") is not None else ""
               ico = vbas.find(path + "ICO").text if vbas.find(path + "ICO") is not None else ""
               dic = vbas.find(path + "DIC").text if vbas.find(path + "DIC") is not None else ""

               zapis_place = ""
               zapis_vlozka = ""
               # Getting the zapis v rejstriku
               if vbas.find(path + "ROR") is not None:
                   zapis_parent = vbas.find(path + "ROR")
                   if zapis_parent.find(path + "SZ") is not None:
                       zapis = zapis_parent.find(path + "SZ")

                       zapis_vlozka = zapis.find(path + "OV").text if zapis.find(path + "OV") is not None else ""
                       if zapis.find(path + "SD") is not None:
                           zapis_place_parent = zapis.find(path + "SD")
                           zapis_place = zapis_place_parent.find(path + "T").text if zapis_place_parent.find(path + "T") is not None else ""

               zapis_rejstrik = ""
               if zapis_place and zapis_vlozka:
                   zapis_rejstrik = "vedeno v obchodním rejstříku, " + zapis_place + ", vložka " + zapis_vlozka

               country = ""
               street = ""
               city = ""
               # Getting the geological information about the company
               if vbas.find(path + "AD") is not None:
                   geological_info = vbas.find(path + "AD")

                   street = geological_info.find(path + "UC").text if geological_info.find(path + "UC") is not None else ""
                   city = geological_info.find(path + "PB").text if geological_info.find(path + "PB") is not None else ""

               # Getting the country
               if vbas.find(path + "AA") is not None:
                   country_parent = vbas.find(path + "AA")
                   country = country_parent.find(path + "NS").text if country_parent.find(path + "NS") is not None else ""

               # Creating the status msg
               not_found = []
               if not name:
                   not_found.append("název firmy")
               if not street:
                   not_found.append("ulici")
               if not city:
                   not_found.append("město")
               if not country:
                   not_found.append("zemi")
               if not ico:
                   not_found.append("IČO")
               if not dic:
                   not_found.append("DIČ")
               if not zapis_rejstrik:
                   not_found.append("zápis v obchodním rejstříku")
               not_found.append("telefoní číslo")
               not_found.append("email")
               not_found.append("web")

               items = [name, street, city, country, ico, dic, zapis_rejstrik, '', '', '']
               if title == "Dodavatelé":
                   items = [name, street, city, country, ico, dic, zapis_rejstrik, '', '', '', '', '', '', '', '', '']
                   not_found.append("bankovní údaje")

               msg = "Ares nalezl a vyplnil všechny data."
               if not_found:
                   first_data = True
                   msg = "Ares neposkytl data: "
                   for item in not_found:
                       if first_data:
                           msg = msg + item
                           first_data = False
                           continue
                       msg = msg + ", " + item

               # Saving the new data from ares to dataframe
               return items

           else:
               print("data nenalezena")

       except requests.exceptions.ConnectionError:
           print("no internet")

   else:
       print("data nenalezena")

@app.route('/get_ico_data', methods=['GET', 'POST'])
def get_ico_data():
    text = request.args.get('jsdata')
    s = auto_fill(text, "")
    print(s)
    return json.dumps(s)

@app.route('/download', methods=['GET', 'POST'])
def download():    
    return send_from_directory(app.root_path, "faktura.pdf", as_attachment=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/faktura", methods = ["GET", "POST"])
def faktura():
    print("in faktura")
    
    items = []
    class Item():
        def __init__(self, polozka, dph, count, price):
            self.delivery_name = polozka
            self.dph = dph
            self.count = count
            self.price = price

    polozky = request.args.getlist("polozka")
    count = request.args.getlist("count")
    price = request.args.getlist("price")
    dphs = request.args.getlist("dph")

    for i in range(len(polozky)):
        item = Item(polozky[i], count[i], price[i], dphs[i])
        items.append(item)

    date = {
        "vystaveni_date": request.args.get("splatnost_date"),
        "zdanpl_date": request.args.get("zdanpl_date"),
        "splatnost_date": request.args.get("vystaveni_date"),
    }


    dodavatel = request.args.get("dodavatel")
    dodavatel_ico = request.args.get("dodavatel_ico")
    dodavatel_dic = request.args.get("ododavatel_dic")
    dodavatel_street = request.args.get("dodavatel_street")
    dodavatel_city = request.args.get("dodavatel_city")
    dodavatel_country = request.args.get("dodavatel_country")
    dodavatel_rejstrik = request.args.get("dodavatel_rejstrik")
    dodavatel_telefon = request.args.get("dodavatel_telefon")
    dodavatel_email = request.args.get("dodavatel_email")
    dodavatel_web = request.args.get("dodavatel_web")

    account_number = request.args.get("account_number")
    bank_number = request.args.get("bank_number")
    konst_cislo = request.args.get("konst_cislo")
    var_cislo = request.args.get("var_cislo")
    iban = request.args.get("iban")
    swift = request.args.get("swift")
    
    dodavatel_list = [dodavatel, dodavatel_street, dodavatel_city, dodavatel_country, dodavatel_ico, dodavatel_dic, dodavatel_rejstrik, dodavatel_telefon, dodavatel_email, dodavatel_web, 
                      account_number, bank_number, iban, swift, konst_cislo, var_cislo]

    odberatel = request.args.get("odberatel")
    odberatel_ico = request.args.get("odberatel_ico")
    odberatel_dic = request.args.get("oodberatel_dic")
    odberatel_street = request.args.get("odberatel_street")
    odberatel_city = request.args.get("odberatel_city")
    odberatel_country = request.args.get("odberatel_country")
    odberatel_rejstrik = request.args.get("odberatel_rejstrik")
    odberatel_telefon = request.args.get("odberatel_telefon")
    odberatel_email = request.args.get("odberatel_email")
    odberatel_web = request.args.get("odberatel_web")
    odberatel_list = [odberatel, odberatel_street, odberatel_city, odberatel_country, odberatel_ico, odberatel_dic, odberatel_rejstrik, odberatel_telefon, odberatel_email, odberatel_web]

    faktura_numbering = request.args.get("faktura_numbering")
    polozka = request.args.get("polozka")
    dph = request.args.get("dph")
    count = request.args.get("count")
    price = request.args.get("price")

    prenesena_dph = request.args.get("prenesena_dph")
    dodavatel_dph = request.args.get("dodavatel_dph")
    qr_platba = request.args.get("qr_platba")
    pdf = request.args.get("pdf")
    vystavila_osoba = request.args.get("vystavila_osoba")


    print("Loading page :)")

    if dodavatel:
        print(dodavatel)
        excel = ExcelWriter(odberatel, dodavatel, dodavatel_list, odberatel_list, items, prenesena_dph, dodavatel_dph, qr_platba, date, "", faktura_numbering, pdf, vystavila_osoba) 
        output = make_response(excel.invoice)
        output.headers["Content-Disposition"] = "attachment; filename=sheet.xlsx"
        output.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return output


    return render_template("index.html", status="")
