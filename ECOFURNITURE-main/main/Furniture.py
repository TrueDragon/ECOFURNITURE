# Furniture class
class Furniture:
    count_id = 0

    def __init__(self,furniture_type, furniture_name, furniture_quantity, furniture_category, furniture_status,
                 furniture_price, furniture_remarks):
        Furniture.count_id += 1
        self.__furniture_id = Furniture.count_id
        self.__furniture_name = furniture_name
        self.__furniture_quantity = furniture_quantity
        self.__furniture_type = furniture_type
        self.__furniture_status = furniture_status
        self.__furniture_category = furniture_category
        self.__furniture_price = furniture_price
        self.__furniture_remarks = furniture_remarks

    def set_furniture_id(self, furniture_id):
        self.__furniture_id = furniture_id

    def get_furniture_id(self):
        return self.__furniture_id

    def set_furniture_name(self, furniture_name):
        self.__furniture_name = furniture_name

    def get_furniture_name(self):
        return self.__furniture_name

    def set_furniture_quantity(self, furniture_quantity):
        self.__furniture_quantity = furniture_quantity

    def get_furniture_quantity(self):
        return self.__furniture_quantity

    def set_furniture_type(self, furniture_type):
        self.__furniture_type = furniture_type

    def get_furniture_type(self):
        return self.__furniture_type

    def set_furniture_status(self, furniture_status):
        self.__furniture_status = furniture_status

    def get_furniture_status(self):
        return self.__furniture_status

    def set_furniture_category(self, furniture_category):
        self.__furniture_category = furniture_category

    def get_furniture_category(self):
        return self.__furniture_category

    def set_furniture_price(self, furniture_price):
        self.__furniture_price = furniture_price

    def get_furniture_price(self):
        return self.__furniture_price

    def set_furniture_remarks(self, furniture_remarks):
        self.__furniture_remarks = furniture_remarks

    def get_furniture_remarks(self):
        return self.__furniture_remarks