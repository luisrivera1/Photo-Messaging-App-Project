class ChatMember:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.chatnames = []


    def getId(self):
        return self.id

    def getUsername(self):
        return self.username

    def getChatname(self):
        return self.chatname