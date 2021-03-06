from datetime import date

from flask import jsonify
from dao.posts import postsDAO
from dao.chats import chatsDAO

import os
from werkzeug.utils import secure_filename


class postHandler:
    def build_post_dict(self, row):
        result = {}
        result['pid'] = row[0]
        result['p_user'] = row[1]
        result['p_photo'] = row[2]
        result['p_message'] = row[3]
        result['p_date'] = row[4]
        return result

    def build_post_dict_UI(self, row, likes, dislikes):
        result = {}

        dao = postsDAO()

        result['pid'] = row[0]
        result['p_user'] = dao.getUsernameById(row[1])
        result['p_photo'] = row[2]

        pid = str(row[0])

        hashtags = dao.getHashtags(pid)
        print(hashtags)

        added = ""

        for hashtag in hashtags:
            added += hashtag[0] + " "

        result['p_message'] = row[3]
        result['p_hashtags'] = added


        print(type(row[4]))
        result['p_date'] = row[4].strftime("%B %d, %Y")
        result['plikes'] = likes
        result['pdislikes'] = dislikes
        return result

    def build_post_likes_dict(self, pid, row):
        result = {}
        result['pid'] = pid
        result['plikes'] = row
        return result

    def build_post_likes_dict2(self, pid):
        result = {}
        result['pid'] = pid
        result['plikes'] = 0
        return result

    def build_post_dislikes_dict(self, pid, row):
        result = {}
        result['pid'] = pid
        result['pdislikes'] = row
        return result

    def build_post_dislikes_dict2(self, pid):
        result = {}
        result['pid'] = pid
        result['pdislikes'] = 0
        return result

    def build_user_post_dislikes_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['ufirstname'] = row[1]
        result['ulastname'] = row[2]
        result['rdate'] = row[3]
        return result

    def build_user_post_likes_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['ufirstname'] = row[1]
        result['ulastname'] = row[2]
        result['rdate'] = row[3]
        return result

    def build_post_replies_dict(self, row):
        result = {}
        result['pid'] = row[0]
        result['puser'] = row[1]
        result['pphoto'] = row[2]
        result['pmessage'] = row[3]
        result['pdate'] = row[4]
        return result

    def build_post_attributes(self, pid, p_user, p_photo, p_message, p_date):
        result = {}
        result['pid'] = pid
        result['puser'] = p_user
        result['pphoto'] = p_photo
        result['pmessage'] = p_message
        result['pdate'] = p_date
        return result

    # def getAllPosts(self):
    #     dao = postsDAO()
    #     posts_list = dao.getAllPosts()
    #     result_list = []
    #     for row in posts_list:
    #         result = self.build_post_dict(row)
    #         result_list.append(result)
    #     return jsonify(Posts=result_list)

    def getAllPosts(self):
        dao = postsDAO()
        posts_list = dao.getAllPosts()
        if not posts_list:
            return jsonify(Error="No post Found")
        result_list = []
        print(posts_list)
        for row in posts_list:
            likes = dao.getPostLikes(row[0])
            dislikes = dao.getPostDislikes(row[0])
            result = self.build_post_dict_UI(row, likes, dislikes)
            result_list.append(result)
        print(result_list)
        return jsonify(Posts=result_list)

    def getPostById(self, pid):
        dao = postsDAO()
        row = dao.getPostById(pid)
        if not row:
            return jsonify(Error="Post with id: " + str(pid) + " Not Found."), 404
        else:
            result = self.build_post_dict(row)
            return jsonify(Post=result)

    def getAllPostsFromChat(self, args):
        cid = int(args['cid'])
        print(cid)
        dao = chatsDAO()
        posts_list = dao.getPostsFromChat(cid)
        result_list = []
        if not posts_list:
            return jsonify(Error="Chat has no posts"), 404
        else:
            for row in posts_list:
                post = self.build_post_dict(row)
                result_list.append(post)
        return jsonify(ChatPosts=result_list)

    def searchPosts(self, args):
        p_chat = args.get("p_chat")
        p_date = args.get("p_date")
        dao = postsDAO()
        post_list = []
        if (len(args) == 2) and p_chat and p_date:
            post_list = dao.getPostsByChatAndDate(p_chat, p_date)
        elif (len(args) == 1) and p_chat:
            post_list = dao.getPostsByChat(p_chat)
        elif (len(args) == 1) and p_date:
            post_list = dao.getPostsByDate(p_date)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in post_list:
            result = self.build_post_dict(row)
            result_list.append(result)
        return jsonify(Posts=result_list)

    def insertPost(self, form, file):
        print("form: ", form)
        if not form:
            return jsonify(Error="You cannot pass null object"), 400
        if len(form) != 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            p_user = form['puser']
            p_photo = form['pphoto']
            p_message = form['pmessage']
            p_date = form['pdate']
            cname = form['cname']

        if p_user and p_photo and p_message and p_date:
            dao = postsDAO()
            if not dao.getUserById(p_user):
                return jsonify(Error="User " + str(p_user) + " not found."), 404
            pid = dao.insertPost(p_user, p_photo, p_message, p_date)
            cid = chatsDAO().getChatByChatName(cname)
            if not cid:
                return jsonify(Error="Chat with name: " + str(cname) + " not found")
            if not dao.insertIntoHas(cid, pid):
                return jsonify(Error="Inserting into table HAS failed")
            result = self.build_post_attributes(pid, p_user, p_photo, p_message, p_date)

            hashtags = dao.getHashtagList(p_message)
            print(hashtags)

            if len(hashtags) > 0:
                for hashtag in hashtags:
                    print(hashtag)
                    hid = dao.insertIntoHashtag(hashtag)
                    dao.insertIntoTagged(pid, hid)
            return jsonify(Post=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deletePost(self, pid):
        dao = postsDAO()
        if not dao.getPostById(pid):
            return jsonify(Error="Post not found."), 404
        else:
            dao.deleteFromHas(pid)
            dao.deleteFromTagged(pid)
            if dao.deletePost(pid) == 1:
                return jsonify(DeleteStatus="Successfully deleted post: " + str(pid)), 200
            return jsonify(Error="Delete Failed"), 400

    def updateLikeDislike(self, args):
        pid = int(args['pid'])
        dao = postsDAO()
        if not dao.getPostById(pid):
            return jsonify(Error="Post Not Found"), 404
        else:
            operation = args['operation']
            if operation == "like":
                return jsonify(PostLikeStatus="Added Like to Post"), 200
            elif operation == "dislike":
                return jsonify(PostDislikeStatus="Added Dislike to Post"), 200
        return jsonify(Error="Unexpected attributes in post request"), 400

    def updatePostReplies(self, form):
        if len(form) != 2:
            return jsonify(Error="Malformed post request"), 400
        else:
            pid = form['pid']
            preply = form['preply']

            if pid and preply:
                dao = postsDAO()
                if not dao.getPostById(pid):
                    return jsonify(Error="Post Not Found"), 404
                else:
                    return jsonify(PostReplyStatus="Added Reply: " + preply), 200
        return jsonify(Error="Unexpected attributes in post reply request"), 400

    def getLikesOfAPost(self, pid):
        dao = postsDAO()
        if not dao.getPostById(pid):
            return jsonify(Error="Post Not Found"), 404
        else:
            row = dao.getPostLikes(pid)
            # if not row:
            #     result = self.build_post_likes_dict2(pid)
            #     return jsonify(LikesOfPost=result)
            result = self.build_post_likes_dict(pid, row)
            return jsonify(LikesOfPost=result)

    def getDisikesOfAPost(self, pid):
        dao = postsDAO()
        if not dao.getPostById(pid):
            return jsonify(Error="Post Not Found"), 404
        else:
            row = dao.getPostDislikes(pid)
            # if not result:
            #     result = self.build_post_dislikes_dict2(pid)
            #     return jsonify(DislikesOfPost=result)
            result = self.build_post_dislikes_dict(pid, row)
            return jsonify(DislikesOfPost=result)

    def getUsersWhoDislikedPost(self, pid):
        dao = postsDAO()
        if not dao.getPostById(pid):
            return jsonify(Error="Post Not Found"), 404
        else:
            result = dao.getUsersWhoDislikedPost(pid)
            if not result:
                return jsonify(Error="No Dislikes for post found")
            print(result)
            result_list = []
            for column in result:
                print(column)
                result_list.append(self.build_user_post_dislikes_dict(column))
            print(result_list)
            return jsonify(UsersWhoDislikedPost=result_list)

    def getUsersWhoLikedPost(self, pid):
        dao = postsDAO()
        if not dao.getPostById(pid):
            return jsonify(Error="Post Not Found"), 404
        else:
            result = dao.getUsersWhoLikedPost(pid)
            if not result:
                return jsonify(Error="No Likes for post found")
            print(result)
            result_list = []
            for column in result:
                print(column)
                result_list.append(self.build_user_post_likes_dict(column))
            print(result_list)
            return jsonify(UsersWhoLikedPost=result_list)

    def getRepliesOfAPost(self, pid):
        dao = postsDAO()
        if not dao.getPostById(pid):
            return jsonify(Error="Post Not Found"), 404
        else:
            result = dao.getPostReplies(pid)
            print(result)
            if not result:
                return jsonify(Error="Post has no replies.")
            result_list = []
            for column in result:
                result_list.append(self.build_post_replies_dict(column))
            return jsonify(RepliesOfPost=result_list)

    def addReplyToPost(self, pid, form):
        dao = postsDAO()

        # validate that post exists
        if not dao.getPostById(pid):
            return jsonify(Error="Post to reply to does not exist,"), 404

        # validate json
        if len(form) != 4:
            return jsonify(Error="Invalid post arguments.")

        else:
            puser = form['puser']
            pphoto = form['pphoto']
            pmessage = form['pmessage']
            pdate = form['pdate']

            if puser and pphoto and pmessage and pdate:
                reply_id = dao.insertPost(puser, pphoto, pmessage, pdate)

                dao.insertIntoIsReply(reply_id, pid)

                hashtags = dao.getHashtagList(pmessage)
                print(hashtags)

                if len(hashtags) > 0:
                    for hashtag in hashtags:
                        print(hashtag)
                        hid = dao.insertIntoHashtag(hashtag)
                        dao.insertIntoTagged(pid, hid)

                return jsonify(Reply="Reply successfully added.")

            else:
                return jsonify(Error="Reply could not be added.")

    def getAllPostsFromChatname(self, args):
        dao = postsDAO()

        chatname = args['chatname']

        post_list = dao.getAllPostsFromChatname(chatname)

        if len(post_list) == 0:
            return jsonify(Error="Chat has no posts"), 404

        else:
            result = []
            for row in post_list:
                likes = dao.getPostLikes(row[0])
                dislikes = dao.getPostDislikes(row[0])
                result.append(self.build_post_dict_UI(row, likes, dislikes))

            return jsonify(Posts=result)

    def getAllOriginalPostsFromChat(self, args):
        dao = postsDAO()

        print(args)

        chatname = args["chatname"]

        post_list = dao.getAllPostsFromChatname(chatname)

        if len(post_list) == 0:
            return jsonify(Error="Chat has no posts."), 404

        else:
            result = []

            replies_temp = dao.getAllReplies()

            replies = []

            new_post_list = []

            for reply in replies_temp:
                replies.append(reply[0])

            for post in post_list:
                if not post[0] in replies:
                    new_post_list.append(post)

            for row in new_post_list:
                likes = dao.getPostLikes(row[0])
                dislikes = dao.getPostDislikes(row[0])
                result.append(self.build_post_dict_UI(row, likes, dislikes))

            return jsonify(Posts=result)

    def createPost(self, form, file, path):
        dao = postsDAO()

        # Assumes form contains post_msg, user_id, cname
        if form and file and len(form) >= 3:
            puser = form['puser']
            pphoto = "http://127.0.0.1:5000" + path + "/" + file.filename
            pmessage = form['pmessage']
            pdate = form['pdate']
            # user_id = form['puser']
            chatName = form['chatName']



            if puser and pphoto and pmessage and pdate:
                temp = pmessage

                p_message = pmessage.split()
                pmessage = ""

                for word in p_message:
                    if not word[0] == "#":
                        pmessage = pmessage + word + " "

                post = dao.insertPost(puser, pphoto, pmessage, pdate)
                post_id, pdate = post['pid'], post['pdate']
                # post_id, post_date = post['post_id'], post['post_date']

                hashtags = dao.getHashtagList(temp)
                print(hashtags)

                if len(hashtags) > 0:
                    for hashtag in hashtags:
                        print(hashtag)
                        hid = dao.insertIntoHashtag(hashtag)
                        dao.insertIntoTagged(post_id, hid)


                # Upload file
                file_secure_name = secure_filename(file.filename)
                file_path = os.path.join(path, file_secure_name)
                file.save(os.path.join(os.getcwd(), file_path[1:]))



                likes = dao.getPostLikes(post_id)
                dislikes = dao.getPostDislikes(post_id)

                cid = chatsDAO().getChatByChatName(chatName)
                if not cid:
                    return jsonify(Error="Chat with name: " + str(chatName) + " not found")
                if not dao.insertIntoHas(cid, post_id):
                    return jsonify(Error="Inserting into table HAS failed")
                row = [post_id, puser, pphoto, pmessage, pdate]

                # result = self.build_post_attributes(post_id, puser, pphoto, pmessage, pdate)
                result = self.build_post_dict_UI(row, likes, dislikes)

                return jsonify(Post=result), 201
            else:
                return jsonify(Error='Malformed POST request'), 400
        else:
            return jsonify(Error='Malformed POST request'), 400

    def updatePostLikes(self, pid, uid):
        dao = postsDAO()
        if not dao.getPostById(pid):
            return jsonify(Error="Post Not Found"), 404
        if not dao.getUserById(uid):
            return jsonify(Error="User " + str(uid) + " not found."), 404
        else:
            if not dao.didUserReact(pid, uid):
                if dao.insertLikeIntoReaction(pid, uid, date.today()) == 1:
                    row = dao.getPostLikes(pid)
                    result = self.build_post_likes_dict(pid, row)
                    return jsonify(UpdatedLikesOfPost=result)
                return jsonify(Error="Like Update failed"), 404
            return jsonify(Error="User " + str(uid) + " has already reacted to post " + str(pid))

    def updatePostDislikes(self, pid, uid):
        dao = postsDAO()
        if not dao.getPostById(pid):
            return jsonify(Error="Post Not Found"), 404
        if not dao.getUserById(uid):
            return jsonify(Error="User " + str(uid) + " not found."), 404
        else:
            if not dao.didUserReact(pid, uid):
                if dao.insertDislikeIntoReaction(pid, uid, date.today()) == 1:
                    row = dao.getPostDislikes(pid)
                    result = self.build_post_dislikes_dict(pid, row)
                    return jsonify(UpdatedDisikesOfPost=result)
                return jsonify(Error="Dislike Update failed"), 404
            return jsonify(Error="User " + str(uid) + " has already reacted to post " + str(pid))
#Anadir comment 
