# Payment class :D
class Payment:
    count_id = 0
    def __init__(self, first_name, last_name, card_no, exp, cvv):
        Payment.count_id += 1
        self.__cust_id = Payment.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__card_no = card_no
        self.__exp = exp
        self.__cvv = cvv

    def set_cust_id(self, cust_id):
        self.__cust_id = cust_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name       

    def set_card_no(self, card_no):
        self.__card_no = card_no

    def set_exp(self, exp):
        self.__exp = exp

    def set_cvv(self, cvv):
        self.__cvv = cvv

    def get_cust_id(self):
        return self.__cust_id

    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name    

    def get_card_no(self):
        return self.__card_no

    def get_exp(self):
        return self.__exp

    def get_cvv(self):
        return self.__cvv


