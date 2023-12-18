import sqlite3 as sq

global conn, cursor


def db_connect() -> None:
    try:
        conn = sq.connect("users_bot.db") # если ее нет, она создается
        cursor = conn.cursor()

        conn.commit()
    except sq.Error as error:
        print("ERROR:", error)

    finally:
        if(conn):
            conn.close()

def table_clients_comp_price(user_id, file_uniq_id, time, price_photo, unn, name_bussines, adress, worker_name, price, code): # загрузка в базу, если чек успешно распознан
    try:
        conn = sq.connect("users_bot.db")
        cursor = conn.cursor()
        sql_execute = ("""INSERT INTO clients (user_id, file_uniq_price_id, time, price_photo, unn, name_bussines, adress, worker_name, price, code)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""")
        sql_params = (user_id, file_uniq_id, time, price_photo, unn, name_bussines, adress, worker_name, price, code)
        cursor.execute(sql_execute, sql_params)
        conn.commit()

    except sq.Error as error:
        print("ERROR:", error)

    finally:
        if(conn):
            conn.close()

def table_clients_comp_product(user_id, photo_product, file_uniq):
    try:
        conn = sq.connect("users_bot.db")
        cursor = conn.cursor()
        sql_execute = """SELECT user_id FROM clients WHERE user_id = ?"""
        cursor.execute(sql_execute, (user_id, ))
        records = cursor.fetchall()

        if records != []:
            sql_execute = """UPDATE clients SET photo_product = ?, file_uniq_product_id = ? WHERE user_id = ?"""
            sql_params = (photo_product, file_uniq, user_id)
            cursor.execute(sql_execute, sql_params)

        conn.commit()

    except sq.Error as error:
        print("ERROR:", error)

    finally:
        if(conn):
            conn.close()


def fetchall_codes():
    try:
        conn = sq.connect("users_bot.db")
        cursor = conn.cursor()
        sql_execute = """SELECT code FROM clients"""
        cursor.execute(sql_execute)
        records = cursor.fetchall()
        conn.commit()

    except sq.Error as error:
        print("ERROR:", error)

    finally:
        if(conn):
            conn.close()

    return records


def workers_service(user_id, phone_number, code, status_code, time, car_info):
    try:
        conn = sq.connect("users_bot.db")
        cursor = conn.cursor()
        sql_execute = """INSERT INTO workers_service (user_id, phone_number, code, status_code, time, car_info) VALUES (?, ?, ?, ?, ?, ?);"""
        sql_params = (user_id, phone_number, code, status_code, time, car_info)
        cursor.execute(sql_execute, sql_params)
        conn.commit()

    except sq.Error as error:
        print("ERROR:", error)

    finally:
        if(conn):
            conn.close()