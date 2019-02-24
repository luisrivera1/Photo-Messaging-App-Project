from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
# import psycopg2
from Objects.Chat import Chat

class chatsDAO:
    def __init__(self):
        self.chat_list = []
        chat1 = Chat("1", "DBChat1", ["Carlos", "Luis"], "Carlos")
        chat2 = Chat("2", "DBChat2", ["Carlos", "Ramon", "Luis"], "Ramon")

        self.chat_list.append(chat1)
        self.chat_list.append(chat2)

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