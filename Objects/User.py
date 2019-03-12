class User:

    def __init__(self, uid, ufirstname, ulastname, uemail, uusername, upassword):
        self.uid = uid
        self.ufirstname = ufirstname
        self.ulastname = ulastname
        self.uemail = uemail
        self.uusername = uusername
        self.upassword = upassword
        self.chat_list = []

    def getId (self):
        return self.uid

    def getFirstName (self):
        return self.uname

    def getLastName(self):
        return self.ulastname

    def getEmail (self):
        return self.uemail

    def getUsername (self):
        return self.uusername

    def getPassword (self):
        return self.upassword

    def addToChatList(self, chatname):
        self.chat_list.append(chatname)

    def removeFromChatList(self, chatname):
        self.chat_list.remove(chatname)