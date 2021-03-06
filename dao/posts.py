from Objects.Post import Post
from dao.users import usersDAO
from dao.chats import chatsDAO
from Objects.User import User
from Objects.Post import Post
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class postsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s host=%s password=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['host'],
                                                                    pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllPosts(self):
        result = []
        cursor = self.conn.cursor()
        query = "select * from Post;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def getHashtags(self, pid):
        result = []
        cursor = self.conn.cursor()
        query = "select htext from Hashtag natural inner join Tagged where hashtag_id = hid and post_id = %s;"
        cursor.execute(query, (pid,))
        for row in cursor:
            result.append(row)
        return result

    def getPostById(self, pid):
        cursor = self.conn.cursor()
        query = "select * from Post where pid = %s;"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        return result

    def postPhotoAndMsgToChat(self, cid, photo, msg):
        dao = chatsDAO()

        postToAdd = Post(4, "clopez36", photo, "new post added", msg)

        for chat in dao.getChatList():
            if chat.getId() == cid:
                chat.addPost(postToAdd)

    #Recently Added
    def getPostsFromUser(self, puser):
        result = []
        for post in self.posts_list:
            temp = []
            if post.getPostUser() == puser:
                for attribute, value in vars(post).items():
                    temp.append(value)
                    result.append(result)
                print(result)
        return result

    #Recently Added
    def getPostHashtags(self, date):
        result= []
        for post in self.posts_list:
            if post.getPostDate() == date:
                message = post.getPostMessage()
                tokens = message.split()
                for token in tokens:
                    if token[0] == "#":
                        result.append(token)

        return result

    def getPopularHashtagDict(self, date):
        hashtag_dict = {}
        print(self.getPostHashtags(date))

        for hashtag in self.getPostHashtags(date):
            print(hashtag)
            if hashtag in hashtag_dict.keys():
                hashtag_dict[hashtag] = hashtag_dict[hashtag] + 1
            else:
                hashtag_dict[hashtag] = 1

        return hashtag_dict

    def getPostPerDayDict(self):
        day_dict = {}
        print(self.posts_list)
        for post in self.posts_list:
            if post.getPostDate() in day_dict.keys():
                day_dict[post.getPostDate()] = day_dict[post.getPostDate()] + 1
            else:
                day_dict[post.getPostDate()] = 1

        print(day_dict)
        return day_dict

    def getLikesPerDayDict(self):
        likes_dict = {}
        for post in self.posts_list:
            if post.getPostDate() in likes_dict.keys():
                likes_dict[post.getPostDate()] = likes_dict[post.getPostDate()] + post.getPostLikes()
            else:
                likes_dict[post.getPostDate()] = post.getPostLikes()

        print(likes_dict)
        return likes_dict

    def getDislikesPerDayDict(self):
        dislikes_dict = {}
        for post in self.posts_list:
            if post.getPostDate() in dislikes_dict.keys():
                dislikes_dict[post.getPostDate()] = dislikes_dict[post.getPostDate()] + post.getPostDislikes()
            else:
                dislikes_dict[post.getPostDate()] = post.getPostDislikes()

        print(dislikes_dict)
        return dislikes_dict

    def getRepliesPerDayDict(self):
        replies_dict = {}
        for post in self.posts_list:
            if post.getPostDate() in replies_dict.keys():
                replies_dict[post.getPostDate()] = replies_dict[post.getPostDate()] + len(post.getPostReplies())
            else:
                replies_dict[post.getPostDate()] = len(post.getPostReplies())

        print(replies_dict)
        return replies_dict


    def getUsersDictByDay(self, date):
        users_dict = {}

        for post in self.posts_list:
            if post.getPostDate() == date:
                if post.getPostUser() in users_dict.keys():
                    users_dict[post.getPostUser()] = users_dict[post.getPostUser()] + 1
                else:
                    users_dict[post.getPostUser()] = 1

        print(users_dict)
        return users_dict

    def getUserPostsByDateDict(self, user, date):
        user_post_dict = {}

        for post in self.posts_list:
            if post.getPostDate() == date and post.getPostUser() == user:
                if post.getPostUser() in user_post_dict.keys():
                    user_post_dict[post.getPostUser()] = user_post_dict[post.getPostUser()] + 1
                else:
                    user_post_dict[post.getPostUser()] = 1

        print(user_post_dict)
        return user_post_dict

    def getPhotoRepliesDict(self, photo):
        photo_reply_dict = {}

        for post in self.posts_list:
            if post.getPostPhoto() == photo:
                photo_reply_dict[post.getPostPhoto()] = len(post.getPostReplies())

        print(photo_reply_dict)
        return photo_reply_dict

    def getPhotoLikesDict(self, photo):
        photo_likes_dict = {}

        for post in self.posts_list:
            if post.getPostPhoto() == photo:
                photo_likes_dict[post.getPostPhoto()] = post.getPostLikes()

        print(photo_likes_dict)
        return photo_likes_dict

    def getPhotoDislikesDict(self, photo):
        photo_dislikes_dict = {}

        for post in self.posts_list:
            if post.getPostPhoto() == photo:
                photo_dislikes_dict[post.getPostPhoto()] = post.getPostDislikes()

        print(photo_dislikes_dict)
        return photo_dislikes_dict

    def getPostLikes(self, pid):
        cursor = self.conn.cursor()
        query = "select * from reaction where post = %s and type = 'like';"
        cursor.execute(query, (pid,))
        result = cursor.rowcount
        return result

    def getPostDislikes(self, pid):
        cursor = self.conn.cursor()
        query = "select * from reaction where post = %s and type = 'dislike';"
        cursor.execute(query, (pid,))
        result = cursor.rowcount
        return result

    def getUsersWhoDislikedPost(self, pid):
        result = []
        cursor = self.conn.cursor()
        query = "select uid, ufirstname, ulastname, rdate from Users natural inner join Reaction where usr = uid and post = %s and type = 'dislike';"
        cursor.execute(query, (pid,))
        for row in cursor:
            result.append(row)
        return result

    def getUsersWhoLikedPost(self, pid):
        result = []
        cursor = self.conn.cursor()
        query = "select uid, ufirstname, ulastname, rdate from Users natural inner join Reaction where usr = uid and post = %s and type = 'like';"
        cursor.execute(query, (pid,))
        for row in cursor:
            result.append(row)
        return result

    def getPostReplies(self, pid):
        result = []
        cursor = self.conn.cursor()
        query = "select * from Post natural inner join isReply where reply_id = pid and original_id = %s;"
        cursor.execute(query, (pid,))
        for row in cursor:
            result.append(row)
        return result

    def insertPost(self, puser, pphoto, pmessage, pdate):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "insert into Post(puser, pphoto, pmessage, pdate) values (%s, %s, %s, %s) returning pid, pdate;"
        cursor.execute(query, (puser, pphoto, pmessage, pdate,))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def insertIntoHas(self, cid, pid):
        cursor = self.conn.cursor()
        query = "insert into has(chat_id, post_id) values (%s, %s);"
        cursor.execute(query, (cid, pid))
        result = cursor.rowcount
        self.conn.commit()
        return result

    def deleteFromHas(self, pid):
        cursor = self.conn.cursor()
        query = "delete from has where post_id = %s;"
        cursor.execute(query, (pid,))
        result = cursor.rowcount
        self.conn.commit()
        print("Result for Has deletion was: " + str(result))
        return result

    def deleteFromTagged(self, pid):
        cursor = self.conn.cursor()
        query = "delete from tagged where post_id = %s;"
        cursor.execute(query, (pid,))
        result = cursor.rowcount
        self.conn.commit()
        print("Result for Post deletion was: " + str(result))
        return result

    def deletePost(self, pid):
        cursor = self.conn.cursor()
        query = "delete from post where pid = %s;"
        cursor.execute(query, (pid,))
        result = cursor.rowcount
        self.conn.commit()
        print("Result for Post deletion was: " + str(result))
        return result

    def insertIntoIsReply(self, rid, pid):
        cursor = self.conn.cursor()
        query = "insert into isReply(reply_id, original_id) values (%s, %s);"
        cursor.execute(query, (rid, pid))
        self.conn.commit()

    def insertIntoHashtag(self, hashtag):
        cursor = self.conn.cursor()
        query = "insert into Hashtag(htext) values (%s) returning hid;"
        cursor.execute(query, (hashtag,))
        result = cursor.fetchone()[0]
        self.conn.commit()
        return result

    def insertIntoTagged(self, pid, hid):
        cursor = self.conn.cursor()
        query = "insert into Tagged(post_id, hashtag_id) values (%s, %s);"
        cursor.execute(query, (pid, hid))
        self.conn.commit()

    def getHashtagList(self, pmessage):
        message = pmessage.split()

        hashtags = []

        for word in message:
            if word[0] == "#":
                hashtags.append(word)

        return hashtags

    def getUserById(self, uid):
        cursor = self.conn.cursor()
        query = "select * from Users where uid = %s;"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        return result

    def getUsernameById(self, uid):
        cursor = self.conn.cursor()
        query = "select uusername from Users where uid = %s;"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()[0]
        return result

    def getAllPostsFromChatname(self, chatname):
        cursor = self.conn.cursor()
        query = "select pid, puser, pphoto, pmessage, pdate from Chat natural inner join Has natural inner join Post where chat_id = cid and post_id = pid and cname = %s;"
        cursor.execute(query, (chatname,))
        result = cursor.fetchall()
        return result

    def getAllReplies(self):
        cursor = self.conn.cursor()
        query = "select reply_id from isReply";
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def insertLikeIntoReaction(self, pid, uid, date):
        cursor = self.conn.cursor()
        query = "insert into reaction(rdate, type, usr, post) values (%s,'like', %s, %s);"
        cursor.execute(query, (date, uid, pid))
        result = cursor.rowcount
        self.conn.commit()
        return result

    def insertDislikeIntoReaction(self, pid, uid, date):
        cursor = self.conn.cursor()
        query = "insert into reaction(rdate, type, usr, post) values (%s,'dislike', %s, %s);"
        cursor.execute(query, (date, uid, pid))
        result = cursor.rowcount
        self.conn.commit()
        return result

    def didUserReact(self, pid, uid):
        cursor = self.conn.cursor()
        query = "select * from reaction where post = %s and usr = %s;"
        cursor.execute(query, (pid, uid))
        result = cursor.fetchone()
        return result
