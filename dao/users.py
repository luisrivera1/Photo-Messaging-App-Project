from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
# import psycopg2
from Objects.User import User

from Objects.Post import Post
from config.dbconfig import pg_config
import psycopg2


class usersDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s host=%s password=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['host'],
                                                                    pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)


    def getAllUsers(self):
        result = []
        cursor = self.conn.cursor()
        query = "select * from Users"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def getUserById(self, uid):
        cursor = self.conn.cursor()
        query = "select * from Users where uid = %s;"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        return result

    # def getUsersByUsernamev2(self, uusername):
    #     for user in self.user_list:
    #         if user.getUsername() == uusername:
    #             return user

    def getUsersByUsername(self, uusername):
        cursor = self.conn.cursor()
        query = "select * from Users where uusername = %s;"
        cursor.execute(query, (uusername,))
        result = cursor.fetchone()
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
        result = []
        cursor = self.conn.cursor()
        query = "select uid, ufirstname, ulastname from users natural inner join contacts where owner_id = %s and contact_id = uid;"
        cursor.execute(query, (uid,))
        for row in cursor:
            result.append(row)
        return result

    def deleteUserFromContactList(self, uid, user):  # removes user from contact list of user with uid
        self.getUserById2(uid).deleteFromContactList(user)

    def insertContact(self, uid, ufirstname, ulastname, uemail):  # *****
        temp = [ufirstname, ulastname, uemail]
        self.getUserById2(uid).appendToContactList(temp)

    def getUserById2(self, uid):  # receives uid and returns a user
        for user in self.user_list:
            if user.getId() == uid:
                return user
