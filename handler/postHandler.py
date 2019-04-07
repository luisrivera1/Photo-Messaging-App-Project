from flask import jsonify
from dao.posts import postsDAO
from dao.chats import chatsDAO

class postHandler:
    def build_post_dict(self, row):
        result = {}
        result['pid'] = row[0]
        result['p_user'] = row[1]
        result['p_photo'] = row[2]
        result['p_message'] = row[3]
        result['p_date'] = row[4]
        return result

    def build_post_likes_dict(self, row):
        result = {}
        result['pid'] = row[0]
        result['plikes'] = row[1]
        return result

    def build_post_likes_dict2(self, pid):
        result = {}
        result['pid'] = pid
        result['plikes'] = 0
        return result

    def build_post_dislikes_dict(self, row):
        result = {}
        result['pid'] = row[0]
        result['pdislikes'] = row[1]
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

    def build_post_attributes(self, pid, p_user, p_photo, p_date,p_likes,p_dislikes,p_replies,p_chat):
        result = {}
        result['pid'] = pid
        result['p_user'] = p_user
        result['p_photo'] = p_photo
        result['p_date'] = p_date
        result['p_likes'] = p_likes
        result['p_dislikes'] = p_dislikes
        result['p_replies'] = p_replies
        result['p_chat'] = p_chat
        return result

    def getAllPosts(self):
        dao = postsDAO()
        posts_list = dao.getAllPosts()
        result_list = []
        for row in posts_list:
            result = self.build_post_dict(row)
            result_list.append(result)
        return jsonify(Posts=result_list)

    def getPostById(self, args):
        pid = int(args['pid'])
        dao = postsDAO()
        row = dao.getPostById(pid)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            post = self.build_post_dict(row)
            return jsonify(Post=post)

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
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in post_list:
            result = self.build_post_dict(row)
            result_list.append(result)
        return jsonify(Posts=result_list)


    def insertPost(self, form):
        print("form: ", form)
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            pid = form['pid']
            p_user = form['p_user']
            p_photo = form['p_photo']
            p_message = form['p_ message']
            p_likes = form['p_likes']
            p_dislikes = form['p_dislikes']
            p_date = form['p_date']
            p_replies = form['p_replies']

        if pid and p_user and p_photo and p_message and p_likes and p_dislikes and p_date and p_replies:
            dao = postsDAO()
            pid = dao.insert(pid, p_user, p_photo, p_message,p_likes,p_dislikes,p_date,p_replies)
            result = self.build_user_attributes(pid, p_user, p_photo, p_message, p_likes,p_dislikes,p_date,p_replies)
            return jsonify(User=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deletePost(self, pid):
        dao = postsDAO()
        if not dao.getUserById(pid):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(pid)
            return jsonify(DeleteStatus="OK"), 200

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
            result = dao.getPostLikes(pid)
            if not result:
                result = self.build_post_likes_dict2(pid)
                return jsonify(LikesOfPost=result)
            result = self.build_post_likes_dict(result)
            return jsonify(LikesOfPost=result)

    def getDisikesOfAPost(self, pid):
        dao = postsDAO()
        if not dao.getPostById(pid):
            return jsonify(Error="Post Not Found"), 404
        else:
            result = dao.getPostDislikes(pid)
            if not result:
                result = self.build_post_dislikes_dict2(pid)
                return jsonify(DislikesOfPost=result)
            result = self.build_post_dislikes_dict(result)
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
