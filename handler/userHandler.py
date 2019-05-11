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

    def build_user_attributes(self, uid, ufirstname, ulastname, uemail, uusername, upassword):
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
        id = None

        try:
            username = args["uusername"]
        except:
            pass
        try:
            id = args["uid"]
        except:
            pass
        dao = usersDAO()
        users_list = []

        if (len(args) == 1) and username:
            users_list = dao.getUsersByUsername(username)
            print(users_list)
        elif (len(args) == 1) and id:
            users_list = dao.getUserById2(id)
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
        if len(form) != 5:
            return jsonify(Error = "Malformed insert user request"), 400
        else:
            ufirstname = form['ufirstname']
            ulastname= form['ulastname']
            uemail = form['uemail']
            uusername = form['uusername']
            upassword = form['upassword']

            if ufirstname and ulastname and uemail and uusername and upassword:
                dao = usersDAO()
                if dao.getUserByEmail(uemail):
                    return jsonify(Error="User with that email already exists. Please try a different one."), 400
                elif dao.getUsersByUsername(uusername):
                    return jsonify(Error="User with that username already exists. Please try a different one."), 400
                uid = dao.insertUser(ufirstname, ulastname, uemail, uusername, upassword)
                login_id = dao.insertToLogin(uusername, upassword)
                if dao.insertToValidates(login_id, uid) == 1:
                    result = self.build_user_attributes(uid, ufirstname, ulastname, uemail, uusername, upassword)
                    return jsonify(User=result), 201
                else:
                    return jsonify(Error="User insertion failed horribly."), 400
            else:
                return jsonify(Error="Unexpected attributes in insert user request"), 400

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
        row = dao.getUserById(uid)
        if not row:
            return jsonify(Error="User " + str(uid) + " not found."), 404
        else:
            dao.deleteUserFromAllContacts(uid)
            if dao.deleteUserFromValidates(uid) == 1 and dao.deleteUser(uid) == 1 and dao.deleteUserFromLogin(row[4], row[5]) == 1:
                return jsonify(DeletedUser=self.build_user_dict(row)), 200
            else:
                return jsonify(Error="Delete failed"), 404

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

        if len(form) != 2:
            return jsonify(ERROR = "Invalid login.")

        else:
            uusername = form['uusername']
            upassword = form['upassword']

            row = dao.validate_login(uusername, upassword)

            if not row:
                return jsonify(LOGIN = "INVALID LOGIN. INVALID CREDENTIALS"),401
            else:
                return jsonify(LOGIN = "LOGIN VALIDATED. USER " + uusername + " SUCCESSFULLY LOGGED IN."),200

    def register_user(self, form):
        dao = usersDAO()

        if len(form) != 5:
            return jsonify(REGISTER = "Invalid registration. Not enough parameters"), 401

        ufirstname = form['ufirstname']
        ulastname = form['ulastname']
        uemail = form['uemail']
        uusername = form['uusername']
        upassword = form['upassword']

        if ufirstname and ulastname and uemail and uusername and upassword:
            row = dao.insertUser(ufirstname, ulastname, uemail, uusername, upassword)
            if not row or dao.getUserByEmail(uemail) or dao.getUsersByUsername(uusername):
                return jsonify(REGISTER="UNSUCCESSFUL REGISTER"), 401
            else:
                lid = dao.insertToLogin(uusername,upassword)
                dao.insertToValidates(lid, row)

                return jsonify(REGISTER="USER " + uusername + " REGISTERED"), 200
        else:
            return jsonify(Error="Unexpected attributes in update request"), 400

    def build_contact_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['ufirstname'] = row[1]
        result['ulastname'] = row[2]
        return result

    def getContactsById(self, uid):
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

    def addToContactList(self, uid, form):
        dao = usersDAO()
        if not dao.getUserById(uid):
            return jsonify(Error="User with id " + str(uid) + " not found."), 404
        else:
            if len(form) == 1:
                cid = form['cid']
                if cid:
                    if not dao.getUserById(cid):
                        return jsonify(Error="Contact User with id " + str(cid) + " not found."), 404
                    elif dao.getContactFromUserId(uid, cid):
                        return jsonify(Error="User with id " + str(uid) + " already has contact with id " + str(cid)), 404
                    result = self.build_contact_attributes(dao.insertContact(uid, cid))
                    print(result)
                    return jsonify(Contact=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in insert contact request"), 400
            elif len(form) == 5:
                ufirstname = form['ufirstname']
                ulastname = form['ulastname']
                uemail = form['uemail']
                uusername = form['uusername']
                upassword = form['upassword']
                if ufirstname and ulastname and uemail and uusername and upassword:
                    if dao.getUserByEmail(uemail):
                        return jsonify(Error="User with that email already exists. Please try a different one."), 400
                    elif dao.getUsersByUsername(uusername):
                        return jsonify(Error="User with that username already exists. Please try a different one."), 400
                    cid = dao.insertUser(ufirstname, ulastname, uemail, uusername, upassword)
                    result = self.build_contact_attributes(dao.insertContact(uid, cid))
                    print(result)
                    return jsonify(Contact=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in insert contact request"), 400
            else:
                return jsonify(Error="Malformed add to contacts request"), 400

    def deleteContact(self, uid, form):  # by contact id OR by uusername
        dao = usersDAO()
        if not dao.getUserById(uid):  # Checks if user is valid.
            return jsonify(Error="User " + str(uid) + " not found"), 404
        if len(form) != 1:
            return jsonify(Error="Malformed delete contact request"), 400
        else:
            cid = None
            uusername = None
            try:
                uusername = form['uusername']
            except:
                pass
            try:
                cid = form['cid']
            except:
                pass
            if cid:
                row = dao.getContactFromUserId(uid, cid)
                if not row:
                    return jsonify(Error="User with id " + str(uid) + " does NOT have contact with id " + str(cid)), 404
                if dao.deleteUserFromContactList(uid, cid) == 1:
                    result = self.build_contact_attributes(row)
                    return jsonify(DeleteContact=result), 200
                else:
                    return jsonify(Error="Delete contact failed."), 400
            elif uusername:
                row = dao.getContactFromUsername(uid, uusername)
                if not row:
                    return jsonify(Error="There is no user with username: " + str(uusername)), 404
                cid = row[3]
                if not dao.getContactFromUserId(uid, cid):
                    return jsonify(Error="User with id " + str(uid) + " does NOT have contact with username " + str(uusername)), 404
                if dao.deleteUserFromContactList(uid, cid) == 1:
                    result = self.build_contact_attributes(row)
                    return jsonify(DeletedContact=result), 200
                else:
                    return jsonify(Error="Delete contact failed."), 400
            else:
                return jsonify(Error="Malformed delete request"), 400

    def build_contact_attributes(self, row):
        result = {}
        result['ufirstname'] = row[0]
        result['ulastname'] = row[1]
        result['uemail'] = row[2]
        return result

    def getUserByIdORUsername(self, form):
        uusername = None
        uid = None
        dao = usersDAO()

        try:
            uusername = form["uusername"]
            result = dao.getUsersByUsername(uusername)
            if not result:
                return jsonify(Error="User not found"), 404
            result = self.build_user_dict(result)
            return jsonify(User=result)
        except:
            pass
        try:
            uid = form["uid"]
            result = dao.getUserById(uid)
            if not result:
                return jsonify(Error="User not found"), 404
            result = self.build_user_dict(result)
            return jsonify(User=result)
        except:
            return jsonify(Error="Malformed query string"), 400


    def getIdByUsername(self, args):
        dao = usersDAO()

        username = args['username']
        user = dao.getUsersByUsername(username)

        if not user:
            return jsonify(Error = "No user exists with that username")

        else:
            return jsonify(ID = user[0])
