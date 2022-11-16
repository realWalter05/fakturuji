import requests
import xml.etree.ElementTree as ET
import mysql.connector, io, string, random
from excel_writer import ExcelWriter
from database_handler import get_firma_data_from_id, get_popisek_by_id


def get_firma_dict(args):
    dodavatel_je_odberatel = 0
    if args.get("dodavatel_je_odberatel") == "on":
        dodavatel_je_odberatel = 1

    dodavatel_je_dodavatel = 0
    if args.get("dodavatel_je_dodavatel") == "on":
        dodavatel_je_dodavatel = 1        


    dodavatel_sifrovat = 0
    if args.get("dodavatel_sifrovat") == "on":
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
        "web" : args.get("dodavatel_web")  if args.get("dodavatel_web") else "",
        "cislo_uctu" : args.get("cislo_uctu")  if args.get("cislo_uctu") else "",
        "cislo_banky" : args.get("cislo_banky")  if args.get("cislo_banky") else "",
        "konst_symbol" : args.get("konst_symbol")  if args.get("konst_symbol") else "",
        "var_symbol" : args.get("var_symbol")  if args.get("var_symbol") else "",
        "iban" : args.get("iban")  if args.get("iban") else "",
        "swift" : args.get("swift") if args.get("swift") else "",
    }   


def get_items(args):
    items = []
    class Item():
        def __init__(self, polozka, dph, count, price, currency):
            self.delivery_name = polozka
            self.dph = dph
            self.count = count
            self.price = price
            self.currency = currency

    polozky = args.getlist("polozka")
    count = args.getlist("count")
    price = args.getlist("price")
    dphs = args.getlist("dph")
    currencies = args.getlist("currency")

    for i in range(len(polozky)):
        item = Item(polozky[i], count[i], price[i], dphs[i], currencies[i])
        items.append(item)  

    return items


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
                       dodavatel[15], dodavatel[16], dodavatel[17], dodavatel[18]]
    odberatel_list = [odberatel[0], f'{odberatel[3]} {odberatel[4]}', 
                    f'{odberatel[5]} {odberatel[6]}', odberatel[7], odberatel[1],
                    odberatel[2], f"{odberatel[8]} {odberatel[9]}", odberatel[10],
                     odberatel[11], odberatel[12]]
    
    description = ""
    if faktura_data["description_id"] != "":
        popisek_id = get_popisek_by_id(user_data, faktura_data["description_id"])
        if popisek_id:
            description = popisek_id[0]["popisek"]

    # Faktura in excel
    excel.create_faktura(dodavatel_list, odberatel_list, items, 1 if faktura_data["typ"] == 1 else 0, 
                        faktura_data["dodavatel_dph"], faktura_data["qr_platba"], date, description, faktura_data["cislo_faktury"],
                        faktura_data["vystaveno"])                                              
    print("done")  


def get_all_faktury(user_data, faktury, polozky): 
    excel = ExcelWriter()  
    for i in range(0, len(faktury)):
        create_faktura_excel(excel, user_data, faktury[i], polozky[i])
    return excel


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
