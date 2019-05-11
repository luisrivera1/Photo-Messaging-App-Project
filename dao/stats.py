from config.dbconfig import pg_config  # from FOLDER.CLASSNAME import FUNCTIONNAME
# import psycopg2
from Objects.User import User

from Objects.Post import Post
from config.dbconfig import pg_config
import psycopg2


class statsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s host=%s password=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['host'],
                                                                    pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    # def getAllStats(self):
    #     result = []
    #     cursor = self.conn.cursor()
    #     query = "select * from Users"
    #     cursor.execute(query)
    #     for row in cursor:
    #         result.append(row)
    #     return result

    def getPostsPerDayByUser(self, uid, dates):
        result = []
        for row in dates:
            cursor = self.conn.cursor()
            query = "select * from post where puser = %s and pdate = %s;"
            cursor.execute(query, (uid, row))
            result.append([row[0].strftime("%B %d, %Y"), cursor.rowcount])
        return result

    def getDatesOfPostsPerDayByUser(self, uid):
        result = []
        cursor = self.conn.cursor()
        query = "select distinct pdate from post where puser = %s order by pdate;"
        cursor.execute(query, (uid,))
        for row in cursor:
            result.append(row)
        return result

    def getPostDatesAvailable(self):
        result = []
        cursor = self.conn.cursor()
        query = "select Distinct pdate from post order by pdate;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def getMostActiveUsers(self, dates):
        result = []
        for row in dates:
            cursor = self.conn.cursor()
            query = "select * from post where pdate = %s;"
            cursor.execute(query, (row,))
            result.append([row[0].strftime("%B %d, %Y"), cursor.rowcount])
        return result


