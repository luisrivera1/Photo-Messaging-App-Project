from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
import psycopg2
from Objects.Chat import Chat

class chatsDAO:
    def __init__(self):
        self.chat_list = []
        self
        Chat1 = Chat("DEFAULT", )

    def getAllChats(self):
        result = []
        for chat in self.chat_list:
            temp = []
            for attribute, value in chat.__dict__.items():
                temp.append(value)
            result.append(temp)
        return result


def getChatById(self, cid):
            cursor = self.conn.cursor()
            query = "select * from chat where cid = %s;"
            cursor.execute(query, (cid,))
            result = cursor.fetchone()
            return result

    def getChatByChatAdmin(self, cadmin):
        cursor = self.conn.cursor()
        query = "select * from chat where cadmin = %s;"
        cursor.execute(query, (cadmin,))
        result = cursor.fetchone()
        return result

    def getChatByChatName(self, cname):
        cursor = self.conn.cursor()
        query = "select * from chat where cname = %s;"
        cursor.execute(query, (cname,))
        result = cursor.fetchone()
        return result

    def insert(self, cname, cmembers, cadmin):
        cursor = self.conn.cursor()
        query = "insert into chats(cname, cmembers, cadmin) values (%s, %s, %s) returning cid;"
        cursor.execute(query, (cname, cmembers, cadmin))
        cid = cursor.fetchone()[0]
        self.conn.commit()
        return cid

    def delete(self, cid):
        cursor = self.conn.cursor()
        query = "delete from chats where cid = %s;"
        cursor.execute(query, (cid,))
        self.conn.commit()
        return cid