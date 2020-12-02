import re
from handlers.mysqlhandlers import *
import json

features = {
    "ноутбуки": ["Диагональ экрана", "Разрешение экрана", "Процессор", "Оперативная память",
                 "Объем и тип внешнего накопителя"],
    "планшеты": ["Диагональ экрана", "Разрешение экрана", "Процессор", "Оперативная память", "Внутренняя память"],
    "мыши": ["DPI", "Тип подключения", "Количество кнопок", "Наличие подсветски (есть/нет)"],
    "клавиатуры": ["Количество кнопок", "Тип", "Тип подключения", "Наличие подсветки"]
}


def check_price_range(msg: str):
    pattern1 = r'^\d+\s?-\s?\d+$'
    pattern2 = r'^\d+ \d+$'

    if re.match(pattern1, msg) or re.match(pattern2, msg):
        return re.findall(r'\d+', msg)
    else:
        return None


def check_moderator(id_user):
    for user in get_moderators():
        if id_user == user["id_user"]:
            return True
    return False


def get_features_template(prod_type):
    template = "<pre>"
    for feature in features[prod_type]:
        template += feature + "\n"
    template += "</pre>"
    return template


def get_characteristic(data, prod_type):
    arr_features = data.split('\n')
    print(arr_features)
    template = ""
    for feature in arr_features:
        template += "{0}:{1}\n".format(features[prod_type][arr_features.index(feature)], feature)
    return template


def shape_and_insert(data):
    arr_features = data["features"].split('\n')
    prod_type = data["product_type"]
    template_features = "{"
    for feature in arr_features:
        template_features += "\"{0}\": \"{1}\", ".format(features[prod_type][arr_features.index(feature)], feature)
    template_features = template_features[:-2]
    template_features += "}"
    insert_into_products(
        (data["product_name"], list(features.keys()).index(data["product_type"])+1, template_features, data["price"], str(data["photos"])))


def get_and_update_basket(user_id, product_id):
    basket = get_basket_from_db(user_id)
    if basket["products"]:
        basket["products"] += ", " + str(product_id)
    else:
        basket["products"] = str(product_id)
    if update_basket(user_id, basket["products"]):
        return True
    return False


def check_and_create_basket(user_id):
    baskets = search_basket(user_id)
    if baskets["count(*)"] == 0:
        create_basket(user_id)
    else:
        return None


def get_template(products):
    for row in products:
        template = "<b>Название:</b> " + row["name"] + "\n\n<pre>"
        features = json.loads(row["feature"])
        for key, value in features.items():
            template += "  {0}: {1}\n".format(key.title(), value)
        template += "</pre>\n"
        template += "<b>Цена: </b>" + str(row["price"]) + "руб"
        templates.append({"template": template, "picture": row["picture"], "id": row["id"]})




