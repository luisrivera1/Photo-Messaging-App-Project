class User:

    def __init__(self, name, email, username):
        self.name = name
        self.email = email
        self.username = username

    def getName (self):
        return self.name

    def getEmail (self):
        return self.email

    def getUsername (self):
        return self.username
