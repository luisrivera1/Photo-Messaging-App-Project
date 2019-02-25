from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
# import psycopg2
from Objects.Chat import Chat
from Objects.User import User

class chatsDAO:
    def __init__(self):
        self.chat_list = []

        Carlos = User(1, "Carlos", "Lopez", "clopez115@gmail.com", "clopez36", "123pescaitoes")
        Ramon = User(2, "Ramon", "Rosado", "ramon.rosado2@upr.edu", "ramoncin", "12345678")
        Luis = User(3, "Luis", "Rivera", "luis.rivera99999@upr.edu", "oLaMeLlAmOlUiS", "password")

        chat1 = Chat("1", "DBChat1", [Carlos, Luis], " clopez36")
        chat2 = Chat("2", "DBChat2", [Carlos, Ramon, Luis], "ramoncin")

        self.chat_list.append(chat1)
        self.chat_list.append(chat2)

    def getChatList(self):
        return self.chat_list

    def getAllChats(self):
        result = []
        for chat in self.chat_list:
            temp = []
            for attribute, value in chat.vars():
                temp.append(value)
            result.append(temp)
        return result

    def getChatById(self, cid):
        result = []
        for chat in self.chat_list:
            if chat.getID() == cid:
                result.append(chat)
            return result

    def getChatByChatAdmin(self, cadmin):
        result = []
        for chat in self.chat_list:
            if chat.getAdmin() == cadmin:
                result.append(chat)
        return result

    def getChatByChatName(self, cname):
        result = []
        for chat in self.chat_list:
            if chat.getName() == cname:
                result.append(chat)
        return result

    def insert(self, cid, cname, cmembers, cadmin):
        temp = Chat(cid, cname, cmembers, cadmin)

        self.chat_list.append(temp)
        return cid

    def delete(self, cid):
        for chat in self.chat_list:
            if chat.getId() == cid:
                self.chat_list.remove(chat)
        return cid

    def addMemberToChat(self, cid, user):
        for chat in self.chat_list:
            if chat.getId() == cid:
                chat.getMembers().append(user)


    def deleteUserFromChat(self, chat, cuser):
        chat.getMembers().remove(cuser)
