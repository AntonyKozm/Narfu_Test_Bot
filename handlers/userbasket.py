import json
from handlers.mysqlhandlers import get_product_by_id, get_basket_from_db
from handlers.checkers import features


class Basket:
    def __init__(self):
        self.num_product = 0
        self.templates = []
        self.products = []

    def get_template_by_id(self, user_id):
        self.get_products_in_basket(user_id)
        for row in self.products:
            template = "<b>Название:</b> " + row["name"] + "\n\n<pre>"
            features = json.loads(row["feature"])
            for key, value in features.items():
                template += "  {0}: {1}\n".format(key.title(), value)
            template += "</pre>\n"
            template += "<b>Цена: </b>" + str(row["price"]) + "руб"
            self.templates.append({"template": template, "picture": row["picture"], "id": row["id"]})

    def get_products_in_basket(self, user_id):
        basket = get_basket_from_db(user_id)
        if basket["products"]:
            for product_id in basket["products"].split(", "):
                self.products.append(get_product_by_id(product_id))

    def get_product(self):
        try:
            template = self.templates[self.num_product]
            self.num_product += 1
            return template
        except IndexError:
            return None

    def get_names(self, user_id):
        self.get_products_in_basket(user_id)
        types = ["Ноутбук", "Планшет", "Мышь", "Клавиатура"]
        temp = ""
        for p in self.products:
            temp += types[int(p["type"])-1] + " " + p["name"] + "\n"
        return temp

    def get_price(self):
        price = 0
        for i in self.products:
            price += int(i["price"])

        return price