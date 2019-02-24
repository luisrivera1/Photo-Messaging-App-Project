class User:

    def __init__(self, uid, uname, uemail, uusername, upassword):
        self.uid = uid
        self.uname = uname
        self.uemail = uemail
        self.uusername = uusername
        self.upassword = upassword

    def getId (self):
        return self.uid

    def getName (self):
        return self.uname

    def getEmail (self):
        return self.uemail

    def getUsername (self):
        return self.uusername

    def getPassword (self):
        return self.upassword
