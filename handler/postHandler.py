from flask import jsonify
from dao.post import postDao


    def build_post_dict(self, row):
        result = {}
        result['pid'] = row[0]
        result['p_user'] = row[1]
        result['p_photo'] = row[2]
        result['p_message'] = row[3]
        result['p_date'] = row[4]
        result['p_likes'] = row[5]
        result['p_dislikes'] = row[6]
        result['p_replies'] = row[7]
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

    def getAllPost(self):
        dao = postsDAO()
        posts_list = dao.getAllPosts()
        result_list = []
        for row in posts_list:
            result = self.build_post_dict(row)
            result_list.append(result)
        return jsonify(Posts=result_list)


    def getPostById(self, pid):
        dao = postsDAO()
        row = dao.getPostById(pid)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            post = self.build_user_dict(row)
            return jsonify(Post=post)

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
            dao = usersDAO()
            pid = dao.insert(uname, username, password, uemail)
            result = self.build_user_attributes(pid, uname, username, password, uemail)
            return jsonify(User=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400


     def insertUserJson(self, json):
        uname = json['uname']
        username = json['username']
        password = json['password']
        uemail = json['uemail']
        if uname and username and password and uemail:
            dao = userDAO()
            uid = dao.insert(uname, username, password, uemail)
            result = self.build_user_attributes(uid, uname, username, password, uemail)
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