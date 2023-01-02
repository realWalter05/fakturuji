import mysql.connector
from python.user_handler import *
from datetime import date


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


def execute_query(sql, data):
	try:
		conn = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  password="",
		  database="faktury"
		)
		cursor = conn.cursor(prepared=True)
		cursor.execute(sql, data)
		conn.commit()

	except mysql.connector.Error as error:
		print(error)

	finally:
		if conn:
			cursor.close()
			conn.close()


def select_data_prepared_query(sql, data):
	conn = None
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
		if conn:
			cursor.close()
			conn.close()


def decrypt_mysql_dict(data_key, result):
	encryptor = Encryptor(data_key)
	decrypted_result = []

	for  listed_dict in result:
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
	conn = None
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
		if conn:
			cursor.close()
			conn.close()


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
			decrypted_result[0]["konst_symbol"],
			decrypted_result[0]["je_odberatel"],
			decrypted_result[0]["je_dodavatel"],
			decrypted_result[0]["je_sifrovano"]
		]
		return customized_result
	return result


def get_faktura_by_id(user_data, faktura_id):
	sql = "SELECT * FROM faktury WHERE user_id=%s AND id=%s;"
	data = (user_data["id"], faktura_id)
	result = select_data_prepared_query(sql, data)
	return result


def get_user_firmy(user_data):
	sql = "SELECT * FROM firmy WHERE user_id=%s AND smazano_uzivatelem=0;"
	data = (user_data["id"],)
	result = select_data_prepared_query(sql, data)
	if result:
		return decrypt_mysql_dict(user_data["data_key"], result)
	return result


def get_user_firmy_limit(user_data, from_firma, to_firma):
	sql = "SELECT * FROM firmy WHERE user_id=%s  AND smazano_uzivatelem=0 ORDER BY id DESC LIMIT %s, %s;"
	data = (user_data["id"], from_firma, to_firma)
	result = select_data_prepared_query(sql, data)
	if result:
		return decrypt_mysql_dict(user_data["data_key"], result)
	return result


def database_add_popisek(user_data, popisek):
	conn = None
	try:
		conn = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  password="",
		  database="faktury"
		)
		cursor = conn.cursor(prepared=True)

		# Add firma
		sql_insert_query = "INSERT INTO popisky (user_id,nazev,popisek,je_sifrovano) VALUES (%s,%s,%s,%s)"

		if popisek["je_sifrovano"]:
			encryptor = Encryptor(user_data["data_key"])
			# Handling data which we dont encrypt
			temp_dict = {
				"je_sifrovano": popisek["je_sifrovano"],
			}
			del popisek["je_sifrovano"]
			popisek = encryptor.encrypt_dict(popisek)
			popisek = {**popisek, **temp_dict}


		# Encrypt the data
		data = (user_data["id"], popisek["nazev"], popisek["popisek"], popisek["je_sifrovano"])
		cursor.execute(sql_insert_query, data)
		conn.commit()
		return "success"

	except mysql.connector.Error as error:
		print(error)
		return "error"
	finally:
		if conn:
			cursor.close()
			conn.close()


def get_user_popisky(user_data):
	sql = "SELECT * FROM popisky WHERE user_id=%s AND smazano_uzivatelem=0;"
	data = (user_data["id"],)
	result = select_data_prepared_query(sql, data)
	if result:
		return decrypt_mysql_dict(user_data["data_key"], result)
	return result


def get_user_popisky_limit(user_data, from_popisek, to_popisek):
	sql = "SELECT * FROM popisky WHERE user_id=%s AND smazano_uzivatelem=0 ORDER BY id DESC LIMIT %s, %s;;"
	data = (user_data["id"], from_popisek, to_popisek)
	result = select_data_prepared_query(sql, data)
	if result:
		return decrypt_mysql_dict(user_data["data_key"], result)
	return result


def get_user_full_sablony(sablony, user_data):
	faktury = []
	for sablona in sablony:
		faktura = get_faktura_by_id(user_data, sablona["faktura_id"])[0]
		dodavatel_id = int(faktura["dodavatel"]) if faktura["dodavatel"] else None
		odberatel_id = int(faktura["odberatel"]) if faktura["odberatel"] else None
		faktura["dodavatel"] = get_firma_data_from_id(user_data, dodavatel_id)[0] if dodavatel_id != None else ""
		faktura["odberatel"] = get_firma_data_from_id(user_data, odberatel_id)[0] if odberatel_id != None else ""
		faktura["nazev"] = sablona["nazev"]
		faktura["sid"] = sablona["sid"]
		faktury.append(faktura)
	return faktury


def get_user_sablony(user_data):
	sql = "SELECT * FROM sablony WHERE user_id=%s;"
	data = (user_data["id"],)
	result = select_data_prepared_query(sql, data)
	return result


def get_user_sablony_limit(user_data, from_sablona, to_sablona):
	sql = "SELECT * FROM sablony WHERE user_id=%s ORDER BY sid DESC LIMIT %s, %s;"
	data = (user_data["id"], from_sablona, to_sablona)
	result = select_data_prepared_query(sql, data)
	return result

def get_user_full_faktury(faktury, user_data):
	for faktura in faktury:
		dodavatel_id = int(faktura["dodavatel"]) if faktura["dodavatel"] else None
		odberatel_id = int(faktura["odberatel"]) if faktura["odberatel"] else None
		faktura["dodavatel"] = get_firma_data_from_id(user_data, dodavatel_id)[0] if dodavatel_id != None else ""
		faktura["odberatel"] = get_firma_data_from_id(user_data, odberatel_id)[0] if odberatel_id != None else ""
	return faktury


def get_user_faktury(user_data):
	sql = "SELECT * FROM faktury WHERE user_id=%s AND je_sablona=0;"
	data = (user_data["id"],)
	result = select_data_prepared_query(sql, data)
	return result


def get_user_faktury_limit(user_data, from_faktura, to_faktura):
	sql = "SELECT * FROM faktury WHERE user_id=%s  AND je_sablona=0 ORDER BY id DESC LIMIT %s, %s;"
	data = (user_data["id"], from_faktura, to_faktura)
	result = select_data_prepared_query(sql, data)
	return result


def filter_user_firmy(result, search_text):
	# Filter_decrypted_data
	filtered_result = []
	for resulted in result:
		if search_text.lower() in resulted["nazev"].lower():
			filtered_result.append(resulted)

	return filtered_result

def get_user_firmy_names(user_data, je_dodavatel, je_odberatel):
	sql = "SELECT id,nazev,je_sifrovano FROM firmy WHERE user_id=%s AND (je_dodavatel=%s OR je_odberatel=%s) AND smazano_uzivatelem=0;"
	data = (user_data["id"], je_dodavatel, je_odberatel)
	result = select_data_prepared_query(sql, data)
	if result:
		result = decrypt_mysql_dict(user_data["data_key"], result)
	return result


def get_database_popisky(user_data, search_text):
	sql = "SELECT id,nazev,popisek,je_sifrovano FROM popisky WHERE user_id=%s AND smazano_uzivatelem=0;"
	data = (user_data["id"],)
	result = select_data_prepared_query(sql, data)

	if result:
		decrypted_result = decrypt_mysql_dict(user_data["data_key"], result)
		# Filter_decrypted_data
		filtered_result = []
		for result in decrypted_result:
			if search_text.lower() in result["nazev"].lower():
				filtered_result.append(result)

		if len(filtered_result) == 1:
			if filtered_result[0]["nazev"] == search_text:
				return decrypted_result
		return filtered_result
	return result


def get_cislo_faktury(user_data, dodavatel_id):
	# Get last number from database
	sql = "SELECT MAX(cislo_faktury) FROM `faktury` WHERE user_id=%s and dodavatel=%s"
	data = (user_data["id"], dodavatel_id)
	last_cislo_faktury = select_data_prepared_query(sql, data)[0]["MAX(cislo_faktury)"]

	# Set default number
	cislo_faktury = str(date.today().year)+str(dodavatel_id)+"01"
	if last_cislo_faktury and type(last_cislo_faktury) != int:
		try:
			# Try to convert to int
			cislo_int = int(last_cislo_faktury)
			cislo_faktury = cislo_int + 1
		except ValueError:
			pass

	return cislo_faktury


def post_to_faktura_table(user_data, args, cursor, conn, je_sifrovano):
	print("posting to faktura table")
	dodavatel_id = args.get("dodavatel_id")
	odberatel_id = args.get("odberatel_id")
	faktura_numbering = args.get("faktura_numbering") if args.get("faktura_numbering") else get_cislo_faktury(user_data, dodavatel_id)

	# Checkboxes
	qr_platba = 1 if args.get("qr_platba") == "on" else 0
	dodavatel_dph = 1 if args.get("dodavatel_dph") == "on" else 0
	typ_faktury = 1 if args.get("prenesena_dph") == "on" else 0

	vystavila_osoba = args.get("vystavila_osoba")
	vystaveni_date = args.get("splatnost_date")
	zdanpl_date = args.get("zdanpl_date")
	splatnost_date = args.get("vystaveni_date")
	description_id = args.get("description_id")
	currency_select = args.get("currency-select")

	# Variables
	variable_title0 = args.get("variable_title0")
	variable_data0 = args.get("variable_data0")
	variable_title1 = args.get("variable_title1")
	variable_data1 = args.get("variable_data1")
	variable_title2 = args.get("variable_title2")
	variable_data2 = args.get("variable_data2")
	variable_title3 = args.get("variable_title3")
	variable_data3 = args.get("variable_data3")

	if description_id == "":
		# Add firma
		sql_insert_query = """INSERT INTO faktury
								(user_id,cislo_faktury,dodavatel,odberatel,typ,dodavatel_dph,
								datum_vystaveni,datum_zdanpl,datum_splatnosti,mena,qr_platba,vystaveno,je_sifrovano,
								variable_title0, variable_data0, variable_title1, variable_data1, variable_title2, variable_data2, variable_title3, variable_data3)
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

		# Encrypt the data
		data = (user_data["id"], faktura_numbering, dodavatel_id, odberatel_id, typ_faktury, dodavatel_dph,
				vystaveni_date, zdanpl_date, splatnost_date, currency_select, qr_platba, vystavila_osoba, je_sifrovano,
				variable_title0, variable_data0, variable_title1, variable_data1, variable_title2, variable_data2, variable_title3, variable_data3)
	if description_id:
		# Add firma
		sql_insert_query = """INSERT INTO faktury
								(user_id,cislo_faktury,dodavatel,odberatel,typ,dodavatel_dph,
								datum_vystaveni,datum_zdanpl,datum_splatnosti,description_id,mena,qr_platba,vystaveno,je_sifrovano,
								variable_title0, variable_data0, variable_title1, variable_data1, variable_title2, variable_data2, variable_title3, variable_data3)
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

		# Encrypt the data
		data = (user_data["id"], faktura_numbering, dodavatel_id, odberatel_id, typ_faktury, dodavatel_dph,
				vystaveni_date, zdanpl_date, splatnost_date, description_id, currency_select, qr_platba, vystavila_osoba, je_sifrovano,
				variable_title0, variable_data0, variable_title1, variable_data1, variable_title2, variable_data2, variable_title3, variable_data3)
	cursor.execute(sql_insert_query, data)
	conn.commit()
	return "success"


def delete_whole_faktura_by_id(user_data, faktura_id):
	delete_faktura_by_id(user_data, faktura_id)
	delete_faktura_polozky_by_id(user_data, faktura_id)
	print("faktura deleted")


def delete_faktura_by_id(user_data, faktura_id):
	sql = "DELETE FROM faktury WHERE id=%s AND user_id=%s;"
	data = (faktura_id, user_data["id"])
	execute_query(sql, data)


def delete_faktura_polozky_by_id(user_data, faktura_id):
	sql = "DELETE FROM polozky WHERE user_id=%s AND faktura_id=%s;"
	data = (user_data["id"], faktura_id)
	execute_query(sql, data)


def delete_popisek_by_id(user_data, popisek_id):
	# We need to check if faktura is being used somewhere and if it is then only deactivate it. Not delete it
	sql = "SELECT * FROM faktury WHERE user_id=%s AND description_id=%s;"
	data = (user_data["id"], popisek_id)
	exists_row_count = len(select_data_prepared_query(sql, data))
	if exists_row_count == 0:
		sql = "DELETE FROM popisky WHERE user_id=%s AND id=%s;"
		data = (user_data["id"], popisek_id)
		execute_query(sql, data)
		print(f"deleting {popisek_id}")
		return

	sql = "UPDATE popisky SET smazano_uzivatelem=1 WHERE id=%s AND user_id=%s;"
	data = (popisek_id, user_data["id"])
	execute_query(sql, data)


def delete_firma_by_id(user_data, firma_id):
	# We need to check if faktura is being used somewhere and if it is then only deactivate it. Not delete it
	sql = "SELECT * FROM faktury WHERE user_id=%s AND (dodavatel=%s OR odberatel=%s);"
	data = (user_data["id"], firma_id, firma_id)
	exists_row_count = len(select_data_prepared_query(sql, data))

	if exists_row_count == 0:
		print(f"deleting then {firma_id}")
		sql = "DELETE FROM firmy WHERE id=%s AND user_id=%s;"
		data = (firma_id, user_data["id"])
		execute_query(sql, data)
		return

	sql = "UPDATE firmy SET smazano_uzivatelem=1 WHERE id=%s AND user_id=%s;"
	data = (firma_id, user_data["id"])
	execute_query(sql, data)


def get_user_items(args):
	print("posting to items table")
	items = []
	polozky = args.getlist("polozka")
	count = args.getlist("count")
	price = args.getlist("price")
	dphs = args.getlist("dph")

	for i in range(len(polozky)):
		if not polozky[i] and not count[i] and not price[i] and not dphs[i]:
			continue
		items.append({
			"dodavka": polozky[i],
			"pocet": count[i],
			"cena": price[i],
			"dph": dphs[i]})
	return items



def post_to_items_table(user_data, args, cursor, conn, last_row, je_sifrovano):
	items = get_user_items(args)
	for item in items:
		# Add firma
		sql_insert_query = """INSERT INTO polozky
								(user_id,faktura_id,dodavka,dph,pocet,cena)
							VALUES (%s,%s,%s,%s,%s,%s)"""

		data = (user_data["id"], last_row, item["dodavka"], str(item["dph"]), str(item["pocet"]), str(item["cena"]))
		if je_sifrovano:
			# Encrypt the data
			encryptor = Encryptor(user_data["data_key"])
			data = (user_data["id"], last_row, encryptor.encrypt_data(item["dodavka"]), encryptor.encrypt_data(item["dph"]),
					encryptor.encrypt_data(item["pocet"]), encryptor.encrypt_data(item["cena"]))
		cursor.execute(sql_insert_query, data)
		conn.commit()
		print("ok")
	return "success"


def post_faktura(user_data, args):
	print("posting faktura")
	conn = None
	try:
		conn = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  password="",
		  database="faktury"
		)
		cursor = conn.cursor(prepared=True)

		print(f" { args }")
		je_sifrovano = 1 if args.get("je_sifrovano") == "on" else 0
		post_to_faktura_table(user_data, args, cursor, conn, je_sifrovano)
		post_to_items_table(user_data, args, cursor, conn, cursor.lastrowid, je_sifrovano)

	except mysql.connector.Error as error:
		print(error)
		return "error"

	finally:
		if conn:
			cursor.close()
			conn.close()


def post_sablona_faktura(user_data, args):
	print("posting faktura")
	conn = None
	try:
		conn = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  password="",
		  database="faktury"
		)
		cursor = conn.cursor(prepared=True)

		print(f" { args }")
		je_sifrovano = 1 if args.get("je_sifrovano") == "on" else 0
		post_to_faktura_table(user_data, args, cursor, conn, je_sifrovano)
		faktura_id = cursor.lastrowid
		post_to_items_table(user_data, args, cursor, conn, cursor.lastrowid, je_sifrovano)
		make_sablona_from_id(user_data, faktura_id, args.get("sablona_name"))

	except mysql.connector.Error as error:
		print(error)
		return "error"

	finally:
		if conn:
			cursor.close()
			conn.close()


def register_user(username, email, password, password_repeat):
	if not username or not password or not password_repeat or not email:
		return "data_error"

	if not password == password_repeat:
		return "not_same_pwd"

	conn = None
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
		sql_insert_query = "INSERT INTO users (username, email, password, data_key) VALUES (%s,%s,%s,%s)"
		hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

		# Creating a random storage key which we will use for data encryption and encode it with password
		data_key = ''.join((secrets.choice(string.ascii_letters) for i in range(32)))
		encoded_data_key = encrypt_data(password, data_key)

		# Push to database
		data = (username, email, hashed, encoded_data_key)
		cursor.execute(sql_insert_query, data)
		conn.commit()
		return "success"

	except mysql.connector.Error as error:
		return "error"
	finally:
		if conn:
			cursor.close()
			conn.close()


def login_user(username, password):
	if not username or not password:
		return "data_error"
	conn = None
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

		if bcrypt.checkpw(password.encode("utf-8"), result[3].encode("utf-8")):
			return result

		return "wrong_pwd"

	except mysql.connector.Error as error:
		print(error)
		return "error"
	finally:
		if conn:
			cursor.close()
			conn.close()


def get_faktury_by_user(user_data):
	sql = "SELECT * FROM faktury WHERE user_id=%s;"
	data = (user_data["id"],)
	return select_data_prepared_query(sql, data)


def get_polozky_by_faktura_id(user_data, faktury):
	conn = None
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
			# Select the data for each faktura
			sql = "SELECT * FROM polozky WHERE faktura_id=%s AND user_id=%s;"
			data = (faktura["id"], user_data["id"])
			cursor.execute(sql, data)
			polozka = cursor.fetchall()
			conn.commit()

			# Get dictionary
			polozka = get_mysql_data_dict(polozka, cursor.column_names)
			listed = []
			if faktura["je_sifrovano"]:
				# Decrypt the data
				encryptor = Encryptor(user_data["data_key"])
				for decrypted in polozka:
					decrypted = encryptor.decrypt_dict(decrypted)

					decrypted["pocet"] = get_number(decrypted["pocet"])
					decrypted["cena"] = get_number(decrypted["cena"])
					decrypted["dph"] = get_number(decrypted["dph"])
					listed.append(decrypted)
				polozky.append(listed)
				continue

			polozky.append(polozka)
		return polozky

	except mysql.connector.Error as error:
		print(error)
		return "error"

	finally:
		if conn:
			cursor.close()
			conn.close()


def get_faktury_by_id(user_data, faktura_id):
	sql = "SELECT * FROM faktury WHERE user_id=%s and id=%s;"
	data = (user_data["id"], faktura_id)
	return select_data_prepared_query(sql, data)


def get_popisek_by_id(user_data, popisek_id):
	sql = "SELECT * FROM popisky WHERE user_id=%s and id=%s;"
	data = (user_data["id"], popisek_id)
	result = select_data_prepared_query(sql, data)
	if result:
		return decrypt_mysql_dict(user_data["data_key"], result)
	return result


def create_faktura_sablona_copy(user_data, faktura_id):
	conn = None
	try:
		conn = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  password="",
		  database="faktury"
		)
		cursor = conn.cursor(prepared=True)

		# Add firma
		sql = """INSERT INTO faktury (user_id,cislo_faktury,dodavatel,odberatel,typ,dodavatel_dph, datum_vystaveni,datum_zdanpl,datum_splatnosti,qr_platba,vystaveno,je_sifrovano, je_sablona)
			 SELECT user_id,cislo_faktury,dodavatel,odberatel,typ,dodavatel_dph, datum_vystaveni,datum_zdanpl,datum_splatnosti,qr_platba,vystaveno,je_sifrovano, 1 FROM faktury WHERE id=%s AND user_id=%s"""
		data = (faktura_id, user_data["id"])

		cursor.execute(sql, data)
		conn.commit()
		return cursor.lastrowid

	except mysql.connector.Error as error:
		print(error)
		return "error"
	finally:
		if conn:
			cursor.close()
			conn.close()


def create_faktura_items_copy(user_data, faktura_id, new_sablona):
	conn = None
	try:
		conn = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  password="",
		  database="faktury"
		)
		cursor = conn.cursor(prepared=True)

		# Add firma
		sql = """INSERT INTO polozky (user_id,faktura_id,dodavka,dph,pocet,cena)
			 SELECT user_id,%s,dodavka,dph,pocet,cena FROM polozky WHERE user_id=%s AND faktura_id=%s"""
		data = (new_sablona, user_data["id"],faktura_id)
		print("new items")
		cursor.execute(sql, data)
		conn.commit()
		return cursor.lastrowid

	except mysql.connector.Error as error:
		print(error)
		return "error"
	finally:
		if conn:
			cursor.close()
			conn.close()



def make_sablona_from_copy_id(user_data, faktura_id, sablona_name):
	sablona_faktury_id = create_faktura_sablona_copy(user_data, faktura_id)
	print(sablona_faktury_id)
	conn = None
	try:
		conn = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  password="",
		  database="faktury"
		)
		cursor = conn.cursor(prepared=True)

		sql_insert_query = "INSERT INTO sablony (nazev,user_id,faktura_id) VALUES (%s,%s,%s)"

		# Encrypt the data
		data = (sablona_name, user_data["id"], sablona_faktury_id)
		cursor.execute(sql_insert_query, data)
		conn.commit()
		create_faktura_items_copy(user_data, faktura_id, sablona_faktury_id)
		return "success"

	except mysql.connector.Error as error:
		print(error)
		return "error"
	finally:
		if conn:
			cursor.close()
			conn.close()


def make_sablona_from_id(user_data, sablona_faktury_id, sablona_name):
	conn = None
	try:
		conn = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  password="",
		  database="faktury"
		)
		cursor = conn.cursor(prepared=True)

		sql_insert_query = "INSERT INTO sablony (nazev,user_id,faktura_id) VALUES (%s,%s,%s)"

		# Encrypt the data
		data = (sablona_name, user_data["id"], sablona_faktury_id)
		cursor.execute(sql_insert_query, data)
		conn.commit()
		return "success"

	except mysql.connector.Error as error:
		print(error)
		return "error"
	finally:
		if conn:
			cursor.close()
			conn.close()


def delete_sablona_by_id(user_data, faktura_id):
	sql = "DELETE FROM sablony WHERE sid=%s AND user_id=%s;"
	data = (faktura_id, user_data["id"])
	execute_query(sql, data)


def get_sablona_by_id(user_data, sablona_sid):
	sql = "SELECT * FROM sablony WHERE user_id=%s and sid=%s;"
	data = (user_data["id"], sablona_sid)
	return select_data_prepared_query(sql, data)


def delete_user_account(user_data, user_id):
	if user_data["id"] == user_id:
		# Double check
		sql = "DELETE FROM users WHERE user_id=%s;"
		data = (user_id, )
		execute_query(sql, data)