class User:
    count_id = 0

    def __init__(self, username, password, user_type):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__username = username
        self.__password = password
        self.__user_type = user_type

    def get_user_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_user_type(self):
        return self.__user_type

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_user_type(self, user_type):
        self.__user_type = user_type