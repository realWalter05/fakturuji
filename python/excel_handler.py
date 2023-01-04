import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from python.excel_writer import ExcelWriter
from python.database_handler import get_firma_data_from_id, get_popisek_by_id, get_faktura_by_id, get_polozky_by_faktura_id
from PIL import Image
from io import BytesIO
import base64
from flask import render_template


def get_faktura_template(user_data, faktura_id):
    faktura_data = get_faktura_by_id(user_data, faktura_id)
    dodavatel = get_firma_data_from_id(user_data, faktura_data[0]["dodavatel"])
    odberatel = get_firma_data_from_id(user_data, faktura_data[0]["odberatel"])
    polozky = get_polozky_by_faktura_id(user_data, faktura_data)[0]
    polozky = get_prices_polozky(polozky)
    dph = get_dph_rates(polozky)
    popisek = get_popisek_by_id(user_data, faktura_data[0]["description_id"])[0]["popisek"] if faktura_data[0]["description_id"] else ""

    faktura_data[0]["mena_ending"] = get_mena_ending(faktura_data[0]["mena"])
    faktura_data[0]["total_bez_dph"] = 0
    faktura_data[0]["total_s_dph"] = 0
    for polozka in polozky:
        faktura_data[0]["total_bez_dph"] += polozka["bez_dph"]
        faktura_data[0]["total_s_dph"] += polozka["s_dph"]

    faktura_data[0]["datum_vystaveni"] = faktura_data[0]["datum_vystaveni"].strftime("%d.%m.%Y")
    faktura_data[0]["datum_zdanpl"] = faktura_data[0]["datum_zdanpl"].strftime("%d.%m.%Y")
    faktura_data[0]["datum_splatnosti"] = faktura_data[0]["datum_splatnosti"].strftime("%d.%m.%Y")

    try:
        if faktura_data[0]["qr_platba"]:
            # qr platba
            buffered = BytesIO()
            response = requests.get("https://api.paylibo.com/paylibo/generator/czech/image?accountNumber="+str(int(dodavatel[13]))+
                            "&bankCode="+str(int(dodavatel[14]))+"&amount="+str(faktura_data[0]["total_s_dph"])+"&currency=CZK&vs="+str(dodavatel[17])+"&size=200")
            image = Image.open(BytesIO(response.content))
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            base_image = img_str.decode("utf-8")
            return render_template("faktura_template_qr.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky, qr_platba_base=base_image, dph=dph, popisek=popisek)
    except Exception as e:
        print(f"{e} detected. Qr platba wont work. It's probably because you entered incorrect banking details...")

    return render_template("faktura_template.html", dodavatel=dodavatel, odberatel=odberatel, faktura_data=faktura_data[0], polozky=polozky, dph=dph, popisek=popisek)


def get_firma_dict(args):
    dodavatel_je_odberatel = 0
    if args.get("dodavatel_je_odberatel") == "on":
        dodavatel_je_odberatel = 1

    dodavatel_je_dodavatel = 0
    if args.get("dodavatel_je_dodavatel") == "on":
        dodavatel_je_dodavatel = 1


    dodavatel_sifrovat = 0
    if args.get("je_sifrovano") == "on":
        dodavatel_sifrovat = 1

    return {
        "name" : args.get("dodavatel_") if args.get("dodavatel_") else "",
        "ico" : args.get("dodavatel_ico")  if args.get("dodavatel_ico") else "",
        "dic" : args.get("dodavatel_dic")  if args.get("dodavatel_dic") else "",
        "street" : args.get("dodavatel_street")  if args.get("dodavatel_street") else "",
        "cislo_popisne" : args.get("dodavatel_cislo_popisne")  if args.get("dodavatel_cislo_popisne") else "",
        "city" : args.get("dodavatel_city")  if args.get("dodavatel_city") else "",
        "psc" : args.get("dodavatel_psc")  if args.get("dodavatel_psc") else "",
        "country" : args.get("dodavatel_country")  if args.get("dodavatel_country") else "",
        "rejstrik" : args.get("dodavatel_rejstrik")  if args.get("dodavatel_rejstrik") else "",
        "vlozka" : args.get("dodavatel_vlozka")  if args.get("dodavatel_vlozka") else "",
        "telefon" : args.get("dodavatel_telefon")  if args.get("dodavatel_telefon") else "",
        "email" : args.get("dodavatel_email")  if args.get("dodavatel_email") else "",
        "web" : args.get("dodavatel_web")  if args.get("dodavatel_web") else "",
        "je_odberatel" : dodavatel_je_odberatel,
        "je_dodavatel" : dodavatel_je_dodavatel,
        "je_sifrovano" : dodavatel_sifrovat,
        "cislo_uctu" : args.get("cislo_uctu")  if args.get("cislo_uctu") else "",
        "cislo_banky" : args.get("cislo_banky")  if args.get("cislo_banky") else "",
        "konst_symbol" : args.get("konst_symbol")  if args.get("konst_symbol") else "",
        "var_symbol" : args.get("var_symbol")  if args.get("var_symbol") else "",
        "iban" : args.get("iban")  if args.get("iban") else "",
        "swift" : args.get("swift") if args.get("swift") else "",
    }


def get_dph_rates(items):
    # Get various dph rates
    dph_rates = []
    for item in items:
        if not str(item["dph"]).replace(',', "").replace('.', "").isnumeric():
            continue
        dph = get_number(str(item["dph"]))
        if dph not in [dph_rate[0] for dph_rate in dph_rates]:
            dph_rates.append([dph, 0])

    # Save which items have which dph rate s
    for dph in dph_rates:
        for item in items:
            if not str(item["dph"]).replace(',', "").replace('.', "").isnumeric():
                continue
            d = get_number(str(item["dph"]))
            if d == dph[0]:
                dph[1] += round((item["s_dph"] - item["bez_dph"]), 2)
    return dph_rates


def get_number(string_number):
    if not string_number:
        return ""
    negative = False

    if "-" in string_number:
        negative = True
        string_number = string_number.replace("-", "")

    if "." in string_number:
        if negative:
            return float(string_number) * -1
        return float(string_number)

    if negative:
        return int(string_number) * -1
    return int(string_number)


def get_mena_ending(mena):
    currencies = {
        "czk" : "Kč",
        "eur" : "€",
        "usd" : "$",
        "gbp" : "£",
    }
    if mena in currencies:
        return currencies[mena]
    return ""


def create_faktura_excel(excel, user_data, faktura_data, items):
    # Getting the form data
    date = {
        "vystaveni_date": faktura_data["datum_vystaveni"],
        "zdanpl_date": faktura_data["datum_zdanpl"],
        "splatnost_date": faktura_data["datum_splatnosti"],
    }

    dodavatel = get_firma_data_from_id(user_data, faktura_data["dodavatel"])
    odberatel = get_firma_data_from_id(user_data, faktura_data["odberatel"])
    dodavatel_list = [dodavatel[0], f'{dodavatel[3]} {dodavatel[4]}',
                    f'{dodavatel[5]} {dodavatel[6]}', dodavatel[7], dodavatel[1],
                    dodavatel[2], f"{dodavatel[8]} {dodavatel[9]}", dodavatel[10],
                     dodavatel[11], dodavatel[12],  dodavatel[13], dodavatel[14],
                       dodavatel[15], dodavatel[16], dodavatel[17], dodavatel[18]] if dodavatel else []
    odberatel_list = [odberatel[0], f'{odberatel[3]} {odberatel[4]}',
                    f'{odberatel[5]} {odberatel[6]}', odberatel[7], odberatel[1],
                    odberatel[2], f"{odberatel[8]} {odberatel[9]}", odberatel[10],
                     odberatel[11], odberatel[12]] if odberatel else []

    mena = get_mena_ending(faktura_data["mena"])
    variable_data = [
        [faktura_data["variable_title0"], faktura_data["variable_data0"]],
        [faktura_data["variable_title1"], faktura_data["variable_data1"]],
        [faktura_data["variable_title2"], faktura_data["variable_data2"]],
        [faktura_data["variable_title3"], faktura_data["variable_data3"]],
    ]

    description = ""
    if faktura_data["description_id"] != "":
        popisek_id = get_popisek_by_id(user_data, faktura_data["description_id"])
        if popisek_id:
            description = popisek_id[0]["popisek"]

    # Faktura in excel
    excel.create_faktura(dodavatel_list, odberatel_list, items, faktura_data["typ"],
                        faktura_data["dodavatel_dph"], mena, faktura_data["qr_platba"], date, description, faktura_data["cislo_faktury"],
                        faktura_data["vystaveno"], variable_data)
    print("done")
    print(items)


def create_jednorazova_faktura_excel(args):
    excel = ExcelWriter()
    # Getting the form data
    date = {
        "vystaveni_date": args.get("vystaveni_date"),
        "zdanpl_date": args.get("zdanpl_date"),
        "splatnost_date": args.get("splatnost_date"),
    }

    dodavatel_list = [args.get('dodavatel_'), args.get('dodavatel_ico'), args.get('dodavatel_dic'),
                    f"{args.get('dodavatel_street')} {args.get('dodavatel_cislo_popisne')}", f"{args.get('dodavatel_city')} {args.get('dodavatel_psc')}",
                    args.get("dodavatel_country"), f"{args.get('dodavatel_rejstrik')} {args.get('dodavatel_vlozka')}", args.get("dodavatel_telefon"),
                    args.get("dodavatel_email"), args.get("dodavatel_web"), args.get("account_number"), args.get("bank_number"), args.get("iban"),
                    args.get("swift"), args.get("var_cislo"), args.get("konst_cislo")]
    odberatel_list = [args.get('odberatel_'), args.get('odberatel_ico'), args.get('odberatel_dic'),
                    f"{args.get('odberatel_street')} {args.get('odberatel_cislo_popisne')}", f"{args.get('odberatel_city')} {args.get('odberatel_psc')}",
                    args.get("odberatel_country"), f"{args.get('odberatel_rejstrik')} {args.get('odberatel_vlozka')}", args.get("odberatel_telefon"),
                    args.get("odberatel_email"), args.get("odberatel_web")]

    items = []
    polozky = args.getlist("polozka")
    count = args.getlist("count")
    price = args.getlist("price")
    dphs = args.getlist("dph")

    for i in range(len(polozky)):
        item = {"dodavka" : polozky[i],
                "pocet" : count[i],
                "cena" : price[i],
                "dph" : dphs[i]}
        items.append(item)

    mena = get_mena_ending(args.get("currency-select"))
    variable_data = [
        [args.get("variable_title0"), args.get("variable_data0")],
        [args.get("variable_title1"), args.get("variable_data1")],
        [args.get("variable_title2"), args.get("variable_data2")],
        [args.get("variable_title3"), args.get("variable_data3")],
    ]

    description = args.get("description")
    typ = 1 if args.get("prenesena_dph") == "on" else 0
    qr_platba = 1 if args.get("qr_platba") == "on" else 0
    print(qr_platba)
    dodavatel_dph = 1 if args.get("dodavatel_dph") == "on" else 0

    # Faktura in excel
    excel.create_faktura(dodavatel_list, odberatel_list, items, typ,
                        dodavatel_dph, mena, qr_platba, date, description, args.get("faktura_numbering"),
                        args.get("vystavila_osoba"), variable_data)
    return excel


def get_all_faktury(user_data, faktury, polozky):
    excel = ExcelWriter()
    for i in range(0, len(faktury)):
        create_faktura_excel(excel, user_data, faktury[i], polozky[i])
    return excel


def get_all_faktury_in_date(user_data, faktury, polozky, ucetnictvi_od, ucetnictvi_do):
    faktury_exist = False

    excel = ExcelWriter()
    for i in range(0, len(faktury)):
        if datetime.strptime(ucetnictvi_od, "%Y-%m-%d") <= datetime.combine(faktury[i]["datum_vystaveni"], datetime.min.time()) \
        and datetime.strptime(ucetnictvi_do, "%Y-%m-%d") >= datetime.combine(faktury[i]["datum_vystaveni"], datetime.min.time()):
            print("getting")
            faktury_exist = True
            create_faktura_excel(excel, user_data, faktury[i], polozky[i])

    if faktury_exist:
        return excel
    return None


def get_prices_polozky(polozky):
    for polozka in polozky:
        polozka["bez_dph"] = round((int(polozka["pocet"]) if polozka["pocet"] else 0) * (int(polozka["cena"]) if polozka["cena"] else 0), 2)
        polozka["s_dph"] = round((polozka["bez_dph"] if polozka["bez_dph"] else 0) + ((polozka["bez_dph"] if polozka["bez_dph"] else 0) / 100) * (int(polozka["dph"]) if polozka["dph"] else 0), 2)
    return polozky


def change_date_format(date):
    splitted =  reversed(date.split("-"))
    return splitted[1] + ". " + splitted[2] + ". " + splitted[3]


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

               country = ""
               street = ""
               cislo_popisne = ""
               psc = ""
               city = ""
               # Getting the geological information about the company
               if vbas.find(path + "AD") is not None:
                   geological_info = vbas.find(path + "AD")

                   street = geological_info.find(path + "UC").text if geological_info.find(path + "UC") is not None else ""
                   if street:
                    cislo_popisne = street.split(" ")[-1]
                    street = street.split(cislo_popisne)[0].strip()

                   city = geological_info.find(path + "PB").text if geological_info.find(path + "PB") is not None else ""
                   if city:
                    psc = city.split(" ")[-1]
                    city = city.split(psc)[0].strip()

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
               if not psc:
                   not_found.append("město")
               if not cislo_popisne:
                   not_found.append("cislo popisne")
               if not country:
                   not_found.append("zemi")
               if not ico:
                   not_found.append("IČO")
               if not dic:
                   not_found.append("DIČ")
               if not zapis_place:
                   not_found.append("zápis v obchodním rejstříku")
               not_found.append("telefoní číslo")
               not_found.append("email")
               not_found.append("web")

               items = [name, ico, dic, street, cislo_popisne, city, psc, country, zapis_place, zapis_vlozka, '', '', '']
               if title == "Dodavatelé":
                   items = [name, ico, dic, street, cislo_popisne, city, psc, country, zapis_place, zapis_vlozka, '', '', '', '', '', '', '', '', '', '', '']
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
