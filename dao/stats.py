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
        query = "select distinct pdate from post order by pdate;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def getReactionsDatesAvailable(self):
        result = []
        cursor = self.conn.cursor()
        query = "select distinct rdate from reaction order by rdate;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def getLikesPerDate(self, dates):
        result = []
        for row in dates:
            cursor = self.conn.cursor()
            query = "select count(*) from Reaction where rdate = %s and type = 'like';"
            cursor.execute(query, (row,))
            result.append([row[0].strftime("%B %d, %Y"), cursor.fetchone()[0]])
        return result

    def getDisikesPerDate(self, dates):
        result = []
        for row in dates:
            cursor = self.conn.cursor()
            query = "select count(*) from Reaction where rdate = %s and type = 'dislike';"
            cursor.execute(query, (row,))
            result.append([row[0].strftime("%B %d, %Y"), cursor.fetchone()[0]])
        return result

    def getMostActivityOfUsers(self, dates):
        result = []
        for row in dates:
            cursor = self.conn.cursor()
            query = "select puser, count(*) from post where pdate = %s group by puser;"
            cursor.execute(query, (row,))
            tempMax = self.getMaxOfActivityUsers(row)
            for row2 in cursor:
                if row2[1] == tempMax:
                    result.append([row[0].strftime("%B %d, %Y"), row2[0]])
        return result

    def getMaxOfActivityUsers(self, date):
        cursor = self.conn.cursor()
        query = "select max(count) from (select puser, count(*) from post where pdate = %s group by puser) as C;"
        cursor.execute(query, (date,))
        return cursor.fetchone()[0]

    def getMostActiveUsers(self):
        result = []
        cursor = self.conn.cursor()
        query = "select * from (select ufirstname, ulastname, count(*) as total from post natural inner join users where uid = puser group by ufirstname, ulastname) as C order by total desc;"
        cursor.execute(query)
        i = 1;
        for row in cursor:
            if i > 3:
                break
            result.append([row[0] + " " + row[1], row[2]])
            i += 1
        return result

    def getTopHashtags(self):
        result = []
        cursor = self.conn.cursor()
        query = "select htext, count(*) as Total from hashtag natural inner join tagged natural inner join post where hid = hashtag_id and pid = post_id group by htext order by Total desc;"
        cursor.execute(query)
        i = 1;
        for row in cursor:
            if i > 3:
                break
            result.append([row[0], row[1]])
            i += 1
        return result

    def isTherePost(self):
        cursor = self.conn.cursor()
        query = "select * from post;"
        cursor.execute(query)
        if cursor.rowcount >= 1:
            return True
        return False

    def getPostsPerDates(self, dates):
        results = []
        for row in dates:
            cursor = self.conn.cursor()
            query = "select * from post where pdate = %s;"
            cursor.execute(query, (row,))
            results.append([row[0].strftime("%B %d, %Y"), cursor.rowcount])
        return results

    def getTrendringHashtags(self, dates):
        result = []
        for row in dates:
            cursor = self.conn.cursor()
            query = "select htext, count(*) as Total from hashtag natural inner join tagged natural inner join post where pdate = %s and  hid = hashtag_id and pid = post_id group by htext order by Total desc;"
            cursor.execute(query, (row,))
            temp = cursor.fetchall()
            # joker = temp[0][0]
            # joker2 = temp[1][0]
            # joker3 = temp[2][0]
            # joker4 = row[0].strftime("%B %d, %Y")
            if len(temp) == 1:
                result.append([row[0].strftime("%B %d, %Y"), [temp[0][0]]])
            elif len(temp) == 2:
                result.append([row[0].strftime("%B %d, %Y"), [temp[0][0], temp[1][0]]])
            else:
                result.append([row[0].strftime("%B %d, %Y"), [temp[0][0], temp[1][0], temp[2][0]]])
            #result.append([joker4, [joker, joker2, joker3]])
        return result

    def getTrendringHashtagsTotal(self, dates):
        result = []
        for row in dates:
            cursor = self.conn.cursor()
            query = "select distinct * from hashtag natural inner join tagged natural inner join post where pdate = %s and pid = post_id and hid = hashtag_id;"
            cursor.execute(query, (row,))
            temp = cursor.rowcount
            # joker = temp[0][0]
            # joker2 = temp[1][0]
            # joker3 = temp[2][0]
            # joker4 = row[0].strftime("%B %d, %Y")
            result.append([row[0].strftime("%B %d, %Y"), temp])
        return result

    def getAvailableTrendingDates(self):
        results = []
        cursor = self.conn.cursor()
        query = "select distinct pdate from post natural inner join tagged natural inner join hashtag where hid = hashtag_id and pid = post_id order by pdate;"
        cursor.execute(query)
        for row in cursor:
            results.append(row)
        return results

    def getRepliesPerDates(self, dates):  # number of replies per date
        results = []
        for row in dates:
            cursor = self.conn.cursor()
            query = "select count(*) as total from isreply natural inner join post where pid = reply_id and pdate = %s;"
            cursor.execute(query, (row,))
            results.append([row[0].strftime("%B %d, %Y"), cursor.fetchone()[0]])
        return results

    def getAvailableRepliesDates(self):
        results = []
        cursor = self.conn.cursor()
        query = "select distinct pdate from isreply natural inner join post where pid = reply_id;"
        cursor.execute(query)
        for row in cursor:
            results.append(row)
        return results
