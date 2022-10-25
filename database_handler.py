import mysql.connector
from user_handler import *
import time


def select_data_prepared_query(sql, data):
    try:
        conn = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="faktury"
        )        
        cursor = conn.cursor(prepared=True)
        
        cursor.execute(sql, data)
        result = cursor.fetchall()
        conn.commit()
        result = get_mysql_data_dict(result, cursor.column_names)
        return result

    except mysql.connector.Error as error:
        print(error)
        return

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")
                 


def decrypt_mysql_dict(data_key, result):
    encryptor = Encryptor(data_key)
    decrypted_result = []   

    for listed_dict in result:
        if listed_dict["je_sifrovano"]:
            dict_result = encryptor.decrypt_dict(listed_dict)
            decrypted_result.append(dict_result)
            continue
        decrypted_result.append(listed_dict)

    return decrypted_result        


def get_mysql_data_dict(rows, column_names):
    result = []
    for row in rows:
        dictionary = dict(zip(column_names, row))
        result.append(dictionary)
    return result


def database_add_firma(user_data, firma):
    try:
        conn = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="faktury"
        )        
        cursor = conn.cursor(prepared=True)

        # Add firma
        sql_insert_query = """INSERT INTO firmy 
                                (user_id, nazev, ico, dic, ulice, cislo_popisne, mesto, psc, zeme, soud_rejstrik,
                                 soudni_vlozka, telefon, email, web, cislo_uctu, cislo_banky, iban, swift, var_symbol,
                                 konst_symbol, je_odberatel, je_dodavatel, je_sifrovano) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        if firma["je_sifrovano"]:
            encryptor = Encryptor(user_data["data_key"])
            # Handling data which we dont encrypt
            temp_dict = {
                "je_odberatel": firma["je_odberatel"],
                "je_dodavatel": firma["je_dodavatel"],
                "je_sifrovano": firma["je_sifrovano"],
            }
            del firma["je_odberatel"]
            del firma["je_dodavatel"]
            del firma["je_sifrovano"]
            firma = encryptor.encrypt_dict(firma)
            firma = {**firma, **temp_dict}
            print(firma)
        

        # Encrypt the data
        data = (user_data["id"], firma["name"], firma["ico"], firma["dic"], firma["street"], firma["cislo_popisne"], firma["city"],
                firma["psc"], firma["country"], firma["rejstrik"], firma["vlozka"], firma["telefon"], firma["email"], 
                firma["web"], firma["cislo_uctu"], firma["cislo_banky"], firma["iban"], firma["swift"], firma["var_symbol"], 
                firma["konst_symbol"], firma["je_odberatel"], firma["je_dodavatel"], firma["je_sifrovano"])
        cursor.execute(sql_insert_query, data)
        conn.commit()
        return "success"

    except mysql.connector.Error as error:
        print(error)
        return "error"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")    


def get_firma_data_from_id(user_data, id):
    sql = "SELECT * FROM firmy WHERE user_id=%s AND id=%s;"
    data = (user_data["id"], id)    
    result = select_data_prepared_query(sql, data)
    if result: 
        decrypted_result = decrypt_mysql_dict(user_data["data_key"], result)
        customized_result = [
            decrypted_result[0]["nazev"],
            decrypted_result[0]["ico"],
            decrypted_result[0]["dic"],
            decrypted_result[0]["ulice"],
            decrypted_result[0]["cislo_popisne"],
            decrypted_result[0]["mesto"],
            decrypted_result[0]["psc"],
            decrypted_result[0]["zeme"],
            decrypted_result[0]["soud_rejstrik"],
            decrypted_result[0]["soudni_vlozka"],
            decrypted_result[0]["telefon"],
            decrypted_result[0]["email"],
            decrypted_result[0]["web"],
            decrypted_result[0]["cislo_uctu"],
            decrypted_result[0]["cislo_banky"],
            decrypted_result[0]["iban"],
            decrypted_result[0]["swift"],
            decrypted_result[0]["var_symbol"],
            decrypted_result[0]["konst_symbol"]
        ]
        return customized_result    
    return result



def get_user_firmy(user_data):
    sql = "SELECT * FROM firmy WHERE user_id=%s;"
    data = (user_data["id"],)
    result = select_data_prepared_query(sql, data)
    if result:
        return decrypt_mysql_dict(user_data["data_key"], result)      
    return result


def get_user_faktury(user_data):
    sql = "SELECT * FROM faktury WHERE user_id=%s;"
    data = (user_data["id"],)
    result = select_data_prepared_query(sql, data)
    return result 


def get_user_firmy_names(user_data, search_text, je_dodavatel, je_odberatel):
    sql = "SELECT id,nazev,je_sifrovano FROM firmy WHERE user_id=%s AND (je_dodavatel=%s OR je_odberatel=%s);"
    data = (user_data["id"], je_dodavatel, je_odberatel)
    result = select_data_prepared_query(sql, data)
    
    if result:
        decrypted_result = decrypt_mysql_dict(user_data["data_key"], result)   
        # Filter_decrypted_data
        filtered_result = []
        for result in decrypted_result:
            if search_text.lower() in result["nazev"].lower():
                filtered_result.append(result)    

        return filtered_result           
    return result          


def post_to_faktura_table(user_data, args, cursor, conn, je_sifrovano):
    print("posting to faktura table")
    dodavatel_id = args.get("dodavatel_id")
    odberatel_id = args.get("odberatel_id")
    faktura_numbering = args.get("faktura_numbering")

    # Checkboxes
    qr_platba = 1 if args.get("qr_platba") == "on" else 0
    dodavatel_dph = 1 if args.get("dodavatel_dph") == "on" else 0
    typ_faktury = 1 if args.get("prenesena_dph") == "on" else 0

    vystavila_osoba = args.get("vystavila_osoba")
    vystaveni_date = args.get("splatnost_date")
    zdanpl_date = args.get("zdanpl_date")
    splatnost_date = args.get("vystaveni_date")

    # Add firma
    sql_insert_query = """INSERT INTO faktury 
                            (user_id,cislo_faktury,dodavatel,odberatel,typ,dodavatel_dph,
                            datum_vystaveni,datum_zdanpl,datum_splatnosti,qr_platba,vystaveno, je_sifrovano)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    # Encrypt the data
    data = (user_data["id"], faktura_numbering, dodavatel_id, odberatel_id, typ_faktury, dodavatel_dph,
            vystaveni_date, zdanpl_date, splatnost_date, qr_platba, vystavila_osoba, je_sifrovano)
    cursor.execute(sql_insert_query, data)
    conn.commit()
    return "success"


def get_user_items(args):
    print("posting to items table")
    items = []
    polozky = args.getlist("polozka")
    count = args.getlist("count")
    price = args.getlist("price")
    dphs = args.getlist("dph")
    currencies = args.getlist("currency")

    for i in range(len(polozky)):
        if not polozky[i] and not count[i] and not price[i] and not dphs[i] and not currencies[i]:
            continue
        items.append({
            "dodavka": polozky[i],
            "pocet": count[i],
            "cena": price[i],
            "dph": dphs[i],
            "mena": currencies[i]})
    return items



def post_to_items_table(user_data, args, cursor, conn, last_row, je_sifrovano):
    items = get_user_items(args)
    for item in items:
        # Add firma
        sql_insert_query = """INSERT INTO polozky 
                                (user_id,faktura_id,dodavka,dph,pocet,cena,mena)
                            VALUES (%s,%s,%s,%s,%s,%s,%s)"""    

        data = (user_data["id"], last_row, item["dodavka"], str(item["dph"]), str(item["pocet"]), str(item["cena"]), item["mena"])
        if je_sifrovano:
            # Encrypt the data
            encryptor = Encryptor(user_data["data_key"])
            data = (user_data["id"], last_row, encryptor.encrypt_data(item["dodavka"]), encryptor.encrypt_data(item["dph"]), 
                    encryptor.encrypt_data(item["pocet"]), encryptor.encrypt_data(item["cena"]), encryptor.encrypt_data(item["mena"]))
        cursor.execute(sql_insert_query, data)
        conn.commit()
        print("ok")
    return "success"          


def post_faktura(user_data, args):
    print("posting faktura")
    try:
        conn = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="faktury"
        )       
        cursor = conn.cursor(prepared=True)
        
        je_sifrovano = 1 if args.get("je_sifrovano") == "on" else 0
        post_to_faktura_table(user_data, args, cursor, conn, je_sifrovano)
        post_to_items_table(user_data, args, cursor, conn, cursor.lastrowid, je_sifrovano)
    
    except mysql.connector.Error as error:
        print(error)
        return "error"
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")        


def register_user(username, password):
    if not username or not password:
        return "data_error"

    try:
        conn = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="faktury"
        )
        cursor = conn.cursor(prepared=True)

        # Check if username exists
        user_check = "SELECT * FROM users WHERE username=%s"
        cursor.execute(user_check, (username, ))
        result = cursor.fetchone()
        if result:
            return "username_taken"

        # Register user
        sql_insert_query = "INSERT INTO users (username, password, data_key) VALUES (%s,%s, %s)"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Creating a random storage key which we will use for data encryption and encode it with password
        data_key = ''.join((secrets.choice(string.ascii_letters) for i in range(32)))
        encoded_data_key = encrypt_data(password, data_key)

        # Push to database
        data = (username, hashed, encoded_data_key)
        cursor.execute(sql_insert_query, data)
        conn.commit()
        return "success"

    except mysql.connector.Error as error:
        return "error"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")    


def login_user(username, password):
    if not username or not password:
        return "data_error"

    try:
        conn = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="faktury"
        )
        cursor = conn.cursor(prepared=True)

        # Check if username exists
        user_check = "SELECT * FROM users WHERE username=%s"
        cursor.execute(user_check, (username, ))
        result = cursor.fetchone()
        if not result:
            return "wrong_pwd"
        conn.commit()

        if bcrypt.checkpw(password.encode("utf-8"), result[2].encode("utf-8")):
            return result
            
        return "wrong_pwd"

    except mysql.connector.Error as error:
        return "error"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")  


def get_faktury_by_user(user_data):
    sql = "SELECT * FROM faktury WHERE user_id=%s;"
    data = (user_data["id"],)
    return select_data_prepared_query(sql, data) 


def get_polozky_by_faktura_id(user_data, faktury):
    try:
        # Get conn
        conn = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="faktury"
        )        
        cursor = conn.cursor(prepared=True)  

        polozky = []
        for faktura in faktury:
            print(faktura)
            print(f"This is faktura {faktura['id']}...")
            # Select the data for each faktura
            sql = "SELECT * FROM polozky WHERE faktura_id=%s AND user_id=%s;"   
            data = (faktura["id"], user_data["id"])
            cursor.execute(sql, data)
            polozka = cursor.fetchall()
            conn.commit()

            # Get dictionary
            polozka = get_mysql_data_dict(polozka, cursor.column_names)  
            print(polozka)
            listed = []
            if faktura["je_sifrovano"]:
                # Decrypt the data
                print("this interesting")
                encryptor = Encryptor(user_data["data_key"])
                for decrypted in polozka:
                    decrypted = encryptor.decrypt_dict(decrypted)
                    decrypted["pocet"] = int(decrypted["pocet"])
                    decrypted["cena"] = int(decrypted["cena"])
                    decrypted["dph"] = int(decrypted["dph"])
                    listed.append(decrypted)
                print(listed)
                polozky.append(listed)
                continue

            polozky.append(polozka)
        return polozky

    except mysql.connector.Error as error:
        print(error)
        return "error"

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")  


def get_faktury_by_id(user_data, faktura_id):
    sql = "SELECT * FROM faktury WHERE user_id=%s and id=%s;"
    data = (user_data["id"], faktura_id)
    return select_data_prepared_query(sql, data)