from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
# import psycopg2
from Objects.Chat import Chat
from Objects.User import User
from Objects.Post import Post

class chatsDAO:
    def __init__(self):
        self.chat_list = []

        Carlos = User(1, "Carlos", "Lopez", "clopez115@gmail.com", "clopez36", "123pescaitoes")
        Ramon = User(2, "Ramon", "Rosado", "ramon.rosado2@upr.edu", "ramoncin", "12345678")
        Luis = User(3, "Luis", "Rivera", "luis.rivera99999@upr.edu", "oLaMeLlAmOlUiS", "password")

        # add chat members
        chat1 = Chat(1, "DBChat1", "clopez36")
        chat1.addToChatMembers(Carlos)
        chat1.addToChatMembers(Luis)
        chat2 = Chat(2, "DBChat2", "ramoncin")
        chat2.addToChatMembers(Carlos)
        chat2.addToChatMembers(Luis)
        chat2.addToChatMembers(Ramon)

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

    def getChatMemberById(self, cid, mem_id):
        result = []
        for chat in self.chat_list:
            if chat.getId() == cid:
                for member in chat.getMembers():
                    if member.getId() == mem_id:
                        for attribute, value in vars(member).items():
                            result.append(value)
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

    def getPostsFromChat(self, cid):  # returns an array of posts
        result = []
        for chat in self.chat_list:
            if chat.getId() == cid:
                for post in chat.getPosts():
                    # for attribute, value in vars(post).items(): # THIS GIVES AN ARRAY NOT A DICT
                    result.append(post)
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

    def insertPostIntoChat(self, cid, post):
        self.getChatById2(cid).addPost(post)