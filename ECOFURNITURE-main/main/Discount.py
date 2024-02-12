# Payment class :D
class Discount:
    count_id = 0

    def __init__(self, code, amount):
        Discount.count_id += 1
        self.__id = Discount.count_id
        self.__code = code
        self.__amount = amount

    def set_id(self, id):
        self.__id = id

    def set_code(self, code):
        self.__code = code

    def set_amount(self, amount):
        self.__amount = amount

    def get_id(self):
        return self.__id

    def get_code(self):
        return self.__code

    def get_amount(self):
        return self.__amount