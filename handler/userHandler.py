from flask import jsonify
from dao.parts import PartsDAO


class Handler:
    def build_user_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['ufirstname'] = row[1]
        result['ulastname'] = row[2]
        result['uemail'] = row[3]
        result['uusername'] = row[4]
        result['upassword'] = row[5]
        return result


    def build_user_attributes(self, pid, uname, username, password, uemail):
        result = {}
        result['uid'] = pid
        result['uname'] = uname
        result['username'] = username
        result['password'] = password
        result['uemail'] = uemail
        return result




    def getAllUsers(self):
        dao = usersDAO()
        users_list = dao.getAllUsers()
        result_list = []
        for row in users_list:
            result = self.build_user_dict(row)
            result_list.append(result)
        return jsonify(Users =result_list)


    def getUserById(self, uid):
        dao = usersDAO()
        row = dao.getUserById(uid)
        if not row:
            return jsonify(Error = "User Not Found"), 404
        else:
            user = self.build_user_dict(row)
            return jsonify(User = user)




    def searchUsers(self, args):
        username = args.get("username")
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



    # def getPostsByUserId(self, uid):
    #     dao = PartsDAO()
    #     if not dao.getPartById(uid):
    #         return jsonify(Error="Part Not Found"), 404
    #     suppliers_list = dao.getSuppliersByPartId(uid)
    #     result_list = []
    #     for row in suppliers_list:
    #         result = self.build_supplier_dict(row)
    #         result_list.append(result)
    #     return jsonify(Suppliers=result_list)
  #Duda
    # def getSuppliersByPartId(self, p_user):
    #     dao = PartsDAO()
    #     if not dao.getPartById(pid):
    #         return jsonify(Error="Part Not Found"), 404
    #     suppliers_list = dao.getSuppliersByPartId(pid)
    #     result_list = []
    #     for row in suppliers_list:
    #         result = self.build_supplier_dict(row)
    #         result_list.append(result)
    #     return jsonify(Suppliers=result_list)

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
                dao = userDAO()
                uid = dao.insert(uid, ufirstname, ulastname, uemail,uusername,upassword)
                result = self.build_user_attributes(uid, ufirstname, ulastname,uemail,uusername,upassword)
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


    def deleteUser(self, uid):
        dao = usersDAO()
        if not dao.getUserById(uid):
            return jsonify(Error = "User not found."), 404
        else:
            dao.delete(uid)
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
                    return jsonify(Error="Unexpected attributes in update request"), 400



    # def build_part_counts(self, part_counts):
    #     result = []
    #     #print(part_counts)
    #     for P in part_counts:
    #         D = {}
    #         D['id'] = P[0]
    #         D['name'] = P[1]
    #         D['count'] = P[2]
    #         result.append(D)
    #     return result
    #
    # def getCountByPartId(self):
    #     dao = PartsDAO()
    #     result = dao.getCountByPartId()
    #     #print(self.build_part_counts(result))
    #     return jsonify(PartCounts = self.build_part_counts(result)), 200
    #


