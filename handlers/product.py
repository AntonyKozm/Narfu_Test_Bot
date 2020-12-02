from handlers.mysqlhandlers import *
from handlers.checkers import features
import json


class Product:
    def __init__(self, prod_type, price_range):
        self.product_name = prod_type
        self.product_id = list(features.keys()).index(prod_type)+1
        self.price_range = price_range
        self.num_product = 0
        self.templates = []

    def get_template(self):
        for row in get_products(self.product_id, self.price_range):
            template = "<b>Название:</b> " + row["name"] + "\n\n<pre>"
            features = json.loads(row["feature"])
            for key, value in features.items():
                template += "  {0}: {1}\n".format(key.title(), value)
            template += "</pre>\n"
            template += "<b>Цена: </b>" + str(row["price"]) + "руб"
            self.templates.append({"template": template, "picture": row["picture"], "id": row["id"]})

    def get_product(self):
        try:
            template = self.templates[self.num_product]
            self.num_product += 1
            return template
        except IndexError:
            return None

    def get_current_product(self):
        try:
            template = self.templates[self.num_product-1]
            return template
        except IndexError as e:
            print(e)

