from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
# import psycopg2
from Objects.Chat import Chat
from Objects.User import User

class chatsDAO:
    def __init__(self):

        Carlos = User(1, "Carlos", "Lopez", "clopez115@gmail.com", "clopez36", "123pescaitoes")
        Ramon = User(2, "Ramon", "Rosado", "ramon.rosado2@upr.edu", "ramoncin", "12345678")
        Luis = User(3, "Luis", "Rivera", "luis.rivera99999@upr.edu", "oLaMeLlAmOlUiS", "password")

        chat1 = Chat(1, "DBChat1", "clopez36")
        chat2 = Chat(2, "DBChat2",  "ramoncin")
        chat3 = Chat(3, "DBChat3", "clopez36")

        chat1.addToChatMembers(Luis.getUsername())
        chat2.addToChatMembers(Carlos.getUsername())
        chat2.addToChatMembers(Luis.getUsername())

        self.chat_list = [chat1, chat2, chat3]


    def getChatList(self):
        return self.chat_list

    def getAllChats(self):
        result = []
        for chat in self.chat_list:
            temp = []
            for attribute, value in vars(chat).items():
                temp.append(value)
            result.append(temp)
        return result

    def getChatByNameAndId(self, cname, cid):
        result = []
        for chat in self.chat_list:
            if chat.getName() == cname and chat.getId() == cid:
                for attribute, value in vars(chat).items():
                    result.append(value)
        return result

    def getChatById(self, cid):
        result = []
        for chat in self.chat_list:
            if chat.getId() == cid:
                for attribute, value in vars(chat).items():
                    result.append(value)
        return result

    def getChatByChatAdmin(self, cadmin):
        result = []
        for chat in self.chat_list:
            if chat.getAdmin() == cadmin:
                for attribute, value in vars(chat).items():
                    result.append(value)
        return result

    def getChatByChatName(self, cname):
        result = []
        for chat in self.chat_list:
            if chat.getName() == cname:
                for attribute, value in vars(chat).items():
                    result.append(value)
        return result

    def insert(self, cid, cname, cmembers, cadmin):
        temp = Chat(cid, cname, cmembers, cadmin)

        self.chat_list.append(temp)
        return cid

    def delete(self, cid, cadmin):
        for chat in self.chat_list:
            if chat.getId() == cid and chat.getAdmin() == cadmin:
                self.chat_list.remove(chat)
                return True
        return False

    def addMemberToChat(self, cid, user):
        for chat in self.chat_list:
            if chat.getId() == cid:
                chat.getMembers().append(user)


    def deleteUserFromChat(self, chat, cuser):
        chat.getMembers().remove(cuser)
