import pymysql
from config import db_settings
from contextlib import closing


def get_connection():
    return pymysql.connect(
        host=db_settings["host"],
        user=db_settings["user"],
        password=db_settings["password"],
        db=db_settings["db"],
        charset=db_settings["charset"],
        cursorclass=db_settings["cursorclass"]
    )


def get_products(type_prod, price_range):
    with closing(get_connection()) as connection:
        with connection.cursor() as cur:
            sql = "select id, name, feature, price, picture from products where (type=%s and price>=%s and price<=%s)"
            cur.execute(sql, (type_prod, price_range["min"], price_range["max"]))
            return cur.fetchall()


def get_product_by_id(product_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cur:
            sql = "select id, name, type, feature, price, picture from products where (id = %s)"
            cur.execute(sql, (product_id, ))
            return cur.fetchone()


def get_moderators():
    with closing(get_connection()) as connection:
        with connection.cursor() as cur:
            cur.execute("select id_user from moderators")
            return cur.fetchall()


def get_basket_from_db(user_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cur:
            sql = "select products from users where (user_id = %s)"
            cur.execute(sql, (user_id, ))
            return cur.fetchone()


def insert_into_products(data):
    with closing(get_connection()) as connection:
        with connection.cursor() as cur:
            try:
                sql = "INSERT INTO products(name, type, feature, price, picture) " \
                                       "VALUES (%s, %s, %s, %s, %s)"
                cur.execute(sql, data)
            except Exception as e:
                print(e)
            finally:
                connection.commit()


def update_basket(user_id, basket):
    with closing(get_connection()) as connection:
        with connection.cursor() as cur:
            try:
                sql = "update users set products = %s where user_id = %s"
                cur.execute(sql, (basket, user_id))
                connection.commit()
                return True
            except:
                return False


def search_basket(user_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cur:
            sql = "select count(*) from users where user_id = %s"
            cur.execute(sql, (user_id, ))
            return cur.fetchone()


def create_basket(user_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cur:
            try:
                sql = "insert into users (user_id) values(%s)"
                cur.execute(sql, (user_id, ))
            except Exception as e:
                print(e)
            connection.commit()


def clear_basket(user_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cur:
            sql = "update users set products = null where (user_id = %s)"
            cur.execute(sql, (user_id, ))
            connection.commit()

