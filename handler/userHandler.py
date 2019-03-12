from flask import jsonify
from dao.users import usersDAO
from dao.posts import postsDAO


class Handler:
    def build_user_dict(self, row):
        result = {}
        print(row)
        result['uid'] = row[0]
        result['ufirstname'] = row[1]
        result['ulastname'] = row[2]
        result['uemail'] = row[3]
        result['uusername'] = row[4]
        result['upassword'] = row[5]
        return result

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

    def build_user_attributes(self, pid, uname, username, password, uemail):
        result = {}
        result['uid'] = pid
        result['uname'] = uname
        result['username'] = username
        result['password'] = password
        result['uemail'] = uemail
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



    def getAllUsers(self):
        dao = usersDAO()
        users_list = dao.getAllUsers()
        result_list = []
        for row in users_list:
            print(row)
            result = self.build_user_dict(row)
            result_list.append(result)
            print(result_list)
        return jsonify(Users =result_list)

    def getAllPost(self):
        dao = usersDAO()
        posts_list = dao.getAllPosts()
        result_list = []
        for row in posts_list:
            result = self.build_post_dict(row)
            result_list.append(result)
        return jsonify(Posts=result_list)

    def getUserById(self, uid):
        dao = usersDAO()
        row = dao.getUserById(uid)
        if not row:
            return jsonify(Error = "User Not Found"), 404
        else:
            user = self.build_user_dict(row)
            return jsonify(User = user)



    def getPostById(self, pid):
        dao = usersDAO()
        row = dao.getPostById(pid)
        if not row:
            return jsonify(Error="Post Not Found"), 404
        else:
            post = self.build_user_dict(row)
            return jsonify(Post=post)

    def searchUsers(self, args):
        print(args)
        username = args.get("uusername")
        email = args.get("uemail")
        dao = usersDAO()
        users_list = []
        if (len(args) == 2) and username and email:
            users_list = dao.getUserByUsersnameAndEmail(username, email)
        elif (len(args) == 1) and username:
            users_list = dao.getUsersBy(username)
        elif (len(args) == 1) and email:
            users_list = dao.getUsersBy(email)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in users_list:
            result = self.build_user_dict(row)
            result_list.append(result)
        return jsonify(Users=result_list)

    def searchPosts(self, args):
        p_chat = args.get("p_chat")
        p_date = args.get("p_date")
        dao = usersDAO()
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

    def insertUser(self, form):
        print("form: ", form)
        if len(form) != 6:
            return jsonify(Error = "Malformed post request"), 400
        else:
            uid = form['uid']
            ufirstname = form['ufirstname']
            ulastname= form['ulastname']
            uemail = form['uemail']
            uusername = form['uusername']
            upassword = form['upassword']

            if uid and ufirstname and ulastname and uemail and uusername and upassword:
                dao = usersDAO()
                uid = dao.insert(uid, ufirstname, ulastname, uemail,uusername,upassword)
                result = self.build_user_attributes(uid, ufirstname, ulastname,uemail,uusername,upassword)
                return jsonify(User=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertPost(self, form):
        print("form: ", form)
        if len(form) != 8:
            return jsonify(Error = "Malformed post request"), 400
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
                pid = dao.insert(pid, p_user, p_photo, p_message, p_likes, p_dislikes, p_date, p_replies)
                result = self.build_user_attributes(pid, p_user, p_photo, p_message, p_likes, p_dislikes, p_date, p_replies)
                return jsonify(User=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def insertUserJson(self, json):
        uname = json['uname']
        username = json['username']
        password = json['password']
        uemail = json['uemail']
        if uname and username and password and uemail:
            dao = usersDAO()
            uid = dao.insert(uname, username, password, uemail)
            result = self.build_user_attributes(uid, uname, username, password, uemail)
            return jsonify(User=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400


    def deleteUser(self, uid):
        dao = usersDAO()
        if not dao.getUserById(uid):
            return jsonify(Error = "User not found."), 404
        else:
            dao.delete(uid)
            return jsonify(DeleteStatus = "OK"), 200

    def deletePost(self, pid):
        dao = postsDAO()
        if not dao.getUserById(pid):
            return jsonify(Error = "Post not found."), 404
        else:
            dao.delete(pid)
            return jsonify(DeleteStatus = "OK"), 200

    def updateUser(self, uid, form):
        dao = usersDAO()
        if not dao.getUserById(uid):
            return jsonify(Error = "User not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                uname = form['uname']
                username = form['username']
                password = form['password']
                uemail = form['uemail']
                if uname and username and password and uemail:
                    dao.update(uid, uname, username, password, uemail)
                    result = self.build_part_attributes(uid, uname, username, password, uemail)
                    return jsonify(User=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in updat e request"), 400

    def validate_login(self, args):
        dao = usersDAO()

        uusername = None
        password = None

        try:
            uusername = args['uusername']
        except:
            pass

        try:
            password = args['upassword']
        except:
            pass

        row = dao.validate_login(uusername, password)

        if not row:
            return jsonify(LOGIN = "INVALID LOGIN. INVALID CREDENTIALS"),401
        else:
             return jsonify(LOGIN = "LOGIN VALIDATED. USER " +  uusername + " SUCCESSFULLY LOGGED IN."),200

    def register_user(self, args):
        print(args)
        uid = int(args['uid'])
        ufirstname = args['ufirstname']
        ulastname = args['ulastname']
        uemail = args['uemail']
        uusername = args['uusername']
        upassword = args['upassword']

        dao = usersDAO()
        row = dao.register_user(uid,ufirstname, ulastname, uemail, uusername, upassword)
        if not row:
                return jsonify(REGISTER = "UNSUCCESSFUL REGISTER"),401
        else:
            return jsonify(REGISTER = "USER " + uusername + " REGISTERED"),200