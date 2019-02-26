from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
# import psycopg2
from Objects.User import User

class usersDAO:
    def __init__(self):
        self.user_list = []
        Carlos = User(1, "Carlos","Lopez", "clopez115@gmail.com", "clopez36", "123pescaitoes")
        Ramon = User(2, "Ramon",  "Rosado", "ramon.rosado2@upr.edu", "ramoncin", "12345678")
        Luis = User(3, "Luis", "Rivera", "luis.rivera99999@upr.edu", "oLaMeLlAmOlUiS", "password")

        self.user_list = [Carlos, Ramon, Luis]



    def getAllUsers(self):
        result = []
        for user in self.user_list:
            temp = []
            for attribute, value in vars(user).items():
                temp.append(value)
            result.append(temp)
        return result

    def getUserById(self, uid):
        result = []
        for user in self.user_list:
            if user.getId() == uid:
                for attribute, value in vars(user).items():
                    result.append(value)
        print(result)
        return result

    def getUsersByUsernamev2(self, uusername):
        for user in self.user_list:
            if user.getUsername() == uusername:
                return user

    def getUserByUsersnameAndId(self, uusername, uid):
        result = []
        for user in self.user_list:
            if user.getUsername() == uusername and user.getId() == uid:
                for attribute, value in vars(user).items():
                    result.append(value)
        return result


    def getUsersByUsername(self, uusername):
        result = []
        for user in self.user_list:
            if user.getUsername() == uusername:
                for attribute, value in vars(user).items():
                    result.append(value)
        return result

    def getUsersByFirstName(self, ufirstname):
        result = []
        for user in self.user_list:
            if user.getFirstName() == ufirstname:
                for attribute, value in vars(user).items():
                    result.append(value)
        return result

    def getUsersByLastName(self, ufirstname):
        result = []
        for user in self.user_list:
            if user.getLastName() == ufirstname:
                for attribute, value in vars(user).items():
                    result.append(value)
        return result

    def getUserByEmail(self, uemail):
        result = []
        for user in self.user_list:
            if user.getEmail() == uemail:
                for attribute, value in vars(user).items():
                    result.append(value)
        return result

    def insert(self, uid, ufirstname, ulastname, uemail, uusername, upassword):
        temp = User(uid, ufirstname, ulastname, uemail, uusername, upassword)
        self.user_list.append(temp)
        return uid

    def delete(self, uid):
        for user in self.user_list:
            if user.getId() == uid:
                self.user_list.remove(user)
        return uid