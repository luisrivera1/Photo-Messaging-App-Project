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

    def build_user_attributes(self, uid, ufirstname,ulastname, uemail, uusername, upassword):
        result = {}
        result['uid'] = uid
        result['ufirstname'] = ufirstname
        result['ulastname'] = ulastname
        result['uemail'] = uemail
        result['uusername'] = uusername
        result['upassword'] = upassword

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
        print("entro?")
        print(args)

        username = None
        email = None

        try:
            username = args["uusername"]
        except:
            pass
        try:
            email = args["uemail"]
        except:
            pass
        dao = usersDAO()
        users_list = []
        if (len(args) == 2) and username and email:
            users_list = dao.getUserByUsernameAndEmail(username, email)
        elif (len(args) == 1) and username:
            users_list = dao.getUsersByUsername(username)
            print(users_list)
        elif (len(args) == 1) and email:
            users_list = dao.getUserByEmail(email)
        else:
            return jsonify(Error = "Malformed query string"), 400

        result_list = self.build_user_dict(users_list)
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

    def updateUser(self, uid, args):
        dao = usersDAO()
        if not dao.getUserById(uid):
            return jsonify(Error = "User not found."), 404
        else:
            if len(args) != 5:
                return jsonify(Error="Malformed update request"), 400
            else:
                ufirstname = args['ufirstname']
                ulastname = args['ulastname']
                uuemail = args['uemail']
                uusername = args['uusername']
                upassword = args['upassword']

                if ufirstname and ulastname and uuemail and uusername and upassword:
                    dao.updateUser(uid, ufirstname, ulastname, uuemail, uusername, upassword)  # NEEDS TO BE IMPLEMENTED
                    result = self.build_user_attributes(uid, ufirstname, ulastname, uuemail, uusername, upassword)
                    return jsonify(User=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

    def validate_login(self, form):
        dao = usersDAO()

        uusername = None
        password = None

        try:
            uusername = form['uusername']
        except:
            pass

        try:
            password = form['upassword']
        except:
            pass

        row = dao.validate_login(uusername, password)

        if not row:
            return jsonify(LOGIN = "INVALID LOGIN. INVALID CREDENTIALS"),401
        else:
            return jsonify(LOGIN = "LOGIN VALIDATED. USER " + uusername + " SUCCESSFULLY LOGGED IN."),200

    def register_user(self, form):
        dao = usersDAO()
        uid = form['uid']
        if dao.getUserById2(uid):
            return jsonify(Error="User not found."), 404
        ufirstname = form['ufirstname']
        ulastname = form['ulastname']
        uemail = form['uemail']
        uusername = form['uusername']
        upassword = form['upassword']
        if uid and ufirstname and ulastname and uemail and uusername and upassword:
            row = dao.register_user(uid, ufirstname, ulastname, uemail, uusername, upassword)
            if not row:
                return jsonify(REGISTER="UNSUCCESSFUL REGISTER"), 401
            else:
                return jsonify(REGISTER="USER " + uusername + " REGISTERED"), 200
        else:
            return jsonify(Error="Unexpected attributes in update request"), 400


    def build_contact_dict(self, row):
        result = {}
        result['ufirstname'] = row[0]
        result['ulastname'] = row[1]
        result['uemail'] = row[2]
        return result

    def getContactsById(self, args):
        uid = int(args['uid'])
        print(uid)
        dao = usersDAO()
        contact_list = dao.getContactListFromUserId(uid)
        print("THIS IS CONTACT LIST")
        print(contact_list)
        result_list = []
        if not contact_list:
            return jsonify(Error="User Not Found"), 404
        else:
            for row in contact_list:
                user = self.build_contact_dict(row)
                result_list.append(user)
            return jsonify(ContactList=result_list)

    def addToContactList(self, args, form):
        uid = int(args['uid'])
        print(uid)
        dao = usersDAO()
        if not dao.getUserById2(uid):
            return jsonify(Error="User not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request"), 400
            else:
                ufirstname = form['ufirstname']
                ulastname = form['ulastname']
                uemail = form['uemail']
                if ufirstname and ulastname and uemail:
                    dao.insertContact(uid, ufirstname, ulastname, uemail)
                    result = self.build_contact_attributes(ufirstname, ulastname, uemail)
                    return jsonify(User=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

    def deleteContact(self, args, form):
        uid = int(args['uid'])
        print(uid)
        dao = usersDAO()
        if not dao.getUserById2(uid):  # Checks if user is valid.
            return jsonify(Error="User not found"), 404
        if len(form) != 3:
            return jsonify(Error="Malformed update request"), 400
        else:
            ufirstname = form['ufirstname']
            ulastname = form['ulastname']
            uemail = form['uemail']
            if ufirstname and ulastname and uemail:
                result = [ufirstname, ulastname, uemail]
                try:
                    dao.deleteUserFromContactList(uid, result)
                    return jsonify(DeleteStatus="OK"), 200
                except:
                    return jsonify(Error="Contact not found."), 404
            else:
                return jsonify(Error="Malformed delete request"), 400

    def build_contact_attributes(self, ufirstname, ulastname, uemail):
        result = {}
        result['ufirstname'] = ufirstname
        result['ulastname'] = ulastname
        result['uemail'] = uemail
        return result
