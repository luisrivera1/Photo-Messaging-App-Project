from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
# import psycopg2
from Objects.User import User
from Objects.Chat import Chat
from Objects.Post import Post

class chatsDAO:
    def __init__(self):
        self.chat_list = []

        Carlos = User(1, "Carlos", "Lopez", "clopez115@gmail.com", "clopez36", "123pescaitoes")
        Ramon = User(2, "Ramon", "Rosado", "ramon.rosado2@upr.edu", "ramoncin", "12345678")
        Luis = User(3, "Luis", "Rivera", "luis.rivera99999@upr.edu", "oLaMeLlAmOlUiS", "password")

        # add chat members
        chat1 = Chat(1, "DBChat1", "clopez36")
        chat1.addToChatMembers(Carlos.getUsername())
        chat1.addToChatMembers(Luis.getUsername())
        chat2 = Chat(2, "DBChat2", "ramoncin")
        chat2.addToChatMembers(Carlos.getUsername())
        chat2.addToChatMembers(Luis.getUsername())
        chat2.addToChatMembers(Ramon.getUsername())

        # add posts

        firstPost = Post(1, "clopez36", "photo.jpg", "First POST!!", "2/24/2019")
        secondPost = Post(2, " ramoncin", "picture.png", "Second POST!!", "2/25/2019")

        chat1.addPost(firstPost)
        chat1.addPost(secondPost)
        chat2.addPost(secondPost)

        self.chat_list.append(chat1)
        self.chat_list.append(chat2)


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


    def deleteUserFromChat(self, cid, mem_id):
        result = []
        for chat in self.chat_list:
            if chat.getId() == cid:
                for member in chat.getMembers():
                    if member.getId() == mem_id:
                        for attribute, value in vars(member).items():
                            result.append(value)
                        chat.removeChatMember(member)
        return result


    def getPostsFromChat(self, cid):
        result = []
        for chat in self.chat_list:
            if chat.getId() == cid:
                for post in chat.getPosts():
                    for attribute, value in vars(post).items():
                        result.append(value)
                print(result)
        return result

        def getChatMemberById(self, cid, mem_id):
            result = []

        for chat in self.chat_list:
            if chat.getId() == cid:
                for member in chat.getMembers():
                    if member.getId() == mem_id:
                        for attribute, value in vars(member).items():
                            result.append(value)
        return result
