from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
# import psycopg2
from Objects.Chat import Chat
from Objects.User import User
from Objects.Post import Post
from config.dbconfig import pg_config
import psycopg2

class chatsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s host=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['host'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getChatList(self):
        return self.chat_list

    def getAllChats(self):
        result = []
        cursor = self.conn.cursor()
        query = "Select * from Chat;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def getChatById(self, cid):
        cursor = self.conn.cursor()
        query = "Select * from Chat where cid=%s;"
        cursor.execute(query, (cid,))
        result = cursor.fetchone()
        print(result)
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
                for attribute, value in vars(chat).items():
                    result.append(value)
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

    def createChat(self, cname, cadmin):
        cursor = self.conn.cursor()
        query = "insert into chat(cname, cadmin) values (%s, %s) returning cid;"
        cursor.execute(query, (cname, cadmin))
        cid = cursor.fetchone()[0]
        self.conn.commit()
        # Now we match the admin to the recently created chat
        query = "insert into ismember(user_id, chat_id) values (%s, %s);"
        cursor.execute(query, (cadmin, cid))
        self.conn.commit()
        return cid

    def deleteChat(self, cid):
        cursor = self.conn.cursor()
        query = "delete from chat where cid = %s;"
        cursor.execute(query, (cid,))
        result = cursor.rowcount
        self.conn.commit()
        print(result)
        return result

    def isAdmin(self, cid, uid):
        try:
            cursor = self.conn.cursor()
            query = "select * from chat where cid = %s and cadmin = %s;"
            cursor.execute(query, (cid, uid))
            if cursor.rowcount == 1:
                return True
            return False
        except:
            return False

    def deleteMembersOfChat(self, cid, cmembers):
        try:
            for row in cmembers:
                cursor = self.conn.cursor()
                query = "delete from ismember where chat_id = %s and user_id = %s;"
                cursor.execute(query, (cid, row))
                self.conn.commit()
            return True
        except:
            return False

    def getChatMembers(self, cid):
        result = []
        cursor = self.conn.cursor()
        query = "select user_id from ismember where chat_id = %s;"
        cursor.execute(query, (cid,))
        for row in cursor:
            result.append(row)
        return result

    def addMemberToChat(self, cid, user):
        for chat in self.chat_list:
            if chat.getId() == cid:
                chat.getMembers().append(user)

    def deleteUserFromChat(self, cid, username):
        for chat in self.chat_list:
            if chat.getId() == cid:
                for member in chat.getMembers():
                    print(chat.getMembers())
                    if member == username:
                       return member
        return None

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

    def getAllUsersFromChat(self, cid):
        result = []
        cursor = self.conn.cursor()
        query = "select uid, ufirstname, ulastname from Chat natural inner join isMember natural inner join Users where cid = chat_id and uid = user_id and chat_id = %s;"
        cursor.execute(query, (cid,))
        for row in cursor:
            result.append(row)
        return result

    def getAdminOfChat(self, cid):
        cursor = self.conn.cursor()
        query = "select uid, ufirstname, ulastname from Users natural inner join Chat where cadmin = uid and cid = %s;"
        cursor.execute(query, (cid,))
        result = cursor.fetchone()
        return result

    def getAllPostsFromChat(self, cid):
        result = []
        cursor = self.conn.cursor()
        query = "select pid, pmessage, puser from has natural inner join post where post_id = pid and chat_id = %s;"
        cursor.execute(query, (cid,))
        for row in cursor:
            result.append(row)
        return result
