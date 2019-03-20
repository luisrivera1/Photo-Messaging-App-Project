from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
# import psycopg2
from Objects.User import User

from Objects.Post import Post

class usersDAO:
    def __init__(self):
        self.user_list = []
        Carlos = User(1, "Carlos","Lopez", "clopez115@gmail.com", "clopez36", "123pescaitoes")
        Ramon = User(2, "Ramon",  "Rosado", "ramon.rosado2@upr.edu", "ramoncin", "12345678")
        Luis = User(3, "Luis", "Rivera", "luis.rivera99999@upr.edu", "oLaMeLlAmOlUiS", "password")
        Walter = User(4, "Walter", "White", "walter.white1@upr.edu", "heisenberg", "crystalmeth")

        self.user_list = [Carlos, Ramon, Luis, Walter]
        self.insertContact(2, "Juan", "delPueblo", "juan.delpueblo@gmail.com")
        self.insertContact(2, "Juan", "delOTROPueblo", "juan.deOTROpueblo@gmail.com")
        self.insertContact(1, "Yo", "Tu", "yoSoloSoyTu@gmail.com")


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
        return result

    def getUsersByUsernamev2(self, uusername):
        for user in self.user_list:
            if user.getUsername() == uusername:
                return user

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

    def getUserByUsernameAndEmail(self, uusername, uemail):
        result = []
        for user in self.user_list:
            if user.getEmail() == uemail and user.getUsername() == uusername:
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

    def validate_login(self, uusername, password):
        user = self.getUsersByUsernamev2(uusername)

        if user is not None:
            return user.getPassword() == password

        return False

    def createUser(self,uid,ufirstname,ulastname,uemail,uusername,upassword):
        return User(uid,ufirstname,ulastname,uemail,uusername,upassword)

    def register_user(self,uid,ufirstname,ulastname,uemail,uusername,upassword):
        for user in self.user_list:
           print((uusername, user.getUsername()),(uid, user.getId()))
           if user.getUsername() == uusername or user.getId() == uid:
               print("Invalid registration, someone with that ID or Username already exists, try again")
               return False
        self.user_list.append(self.createUser(uid,ufirstname, ulastname, uemail, uusername, upassword))
        return True

    # def postPhotoAndMsgToChat(self, cid, photo, msg):
    #     dao = chatsDAO()
    #
    #     postToAdd = Post(4, "clopez36", photo, "new post added", msg)
    #
    #     for chat in dao.getChatList():
    #         if chat.getId() == cid:
    #             chat.addPost(postToAdd)

    def addToContactList(self, uid, user):
        self.getUserById2(uid).appendToContactList(user)

    def getContactListFromUserId(self, uid):  # returns a contact_list (array of contacts)
        return self.getUserById2(uid).getContactList()

    def deleteUserFromContactList(self, uid, user):  # removes user from contact list of user with uid
        self.getUserById2(uid).deleteFromContactList(user)

    def insertContact(self, uid, ufirstname, ulastname, uemail):  # *****
        temp = [ufirstname, ulastname, uemail]
        self.getUserById2(uid).appendToContactList(temp)

    def getUserById2(self, uid):  # receives uid and returns a user
        for user in self.user_list:
            if user.getId() == uid:
                return user
