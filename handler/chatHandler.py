from flask import jsonify
from dao.chats import chatsDAO


class chatHandler:
    def build_chats_dict(self, row):
        result = {}
        result['cid'] = row[0]
        result['cname'] = row[1]
        result['cmembers'] = row[2]
        result['cadmin'] = row[3]

        return result

    def build_chats_attributes(self, cid, cname, cmembers, cadmin):
        result = {}
        result['cid'] = cid
        result['cname'] = cname
        result['cmembers'] = cmembers
        result['cadmin'] = cadmin

        return result

    def getAllChats(self):
        dao = chatsDAO()
        chats_list = dao.getAllChats()
        result_list = []
        for row in chats_list:
            result = self.build_chats_dict(row)
            result_list.append(result)
        print(result_list)
        return jsonify(Chats=result_list)

    def getChatsById(self, cid):
        dao = chatsDAO()
        row = dao.getChatById(cid)
        if not row:
            return jsonify(Error="Chat Not Found"), 404
        else:
            chats = self.build_chats_dict(row)
            return jsonify(Chats=chats)

        def getChatMemberByID(self, chat_id, mem_id):
            dao = chatsDAO()

        row = dao.getChatMemberById(chat_id, mem_id)
        if not row:
            return jsonify(Error="Member Not Found"), 404

        else:
            member = self.build_chats_dict(row)
            return jsonify(User=member)

    def searchChats(self, args):
        chatname = None
        cid = None

        try:
            chatname = args['cname']
        except:
            pass

        try:
            cid = args['cid']
            cid = int(cid)
        except:
            pass

        dao = chatsDAO()

        if (len(args) == 2) and chatname and cid:
            chats_list = dao.getChatByNameAndId(chatname, cid)
        elif (len(args) == 1) and chatname:
            chats_list = dao.getChatByChatName(chatname)
        elif (len(args) == 1) and cid:
            chats_list = dao.getChatById(cid)
        else:
            return jsonify(Error="Malformed query string"), 400

        result_list = []
        result = self.build_chats_dict(chats_list)
        result_list.append(result)
        return jsonify(Chats=result_list)

    def insertChat(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            cid = form['cid']
            cname = form['cname']
            cmembers = form['cmembers']
            cadmin = form['cadmin']

            if cid and cname and cmembers and cadmin:
                dao = chatsDAO()
                cid = dao.insert(cid, cname, cmembers, cadmin)
                result = self.build_user_attributes(cid, cname, cmembers, cadmin)
                return jsonify(Chat=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertChatJson(self, json):
        cid = json['cid']
        cname = json['cname']
        cmembers = json['cmembers']
        cadmin = json['cadmin']
        if cid and cname and cmembers and cadmin:
            dao = chatsDAO()
            cid = dao.insert(cid, cname, cmembers, cadmin)
            result = self.build_user_attributes(cid, cname, cmembers, cadmin)
            return jsonify(Chat=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deleteChat(self, args):
        dao = chatsDAO()
        cid = None
        cadmin = None

        try:
            cid = args['cid']
            cid = int(cid)
        except:
            pass
        try:
            cadmin = args['cadmin']
        except:
            pass

        if not dao.getChatById(cid):
            return jsonify(Error="No chat by that ID found. Delete operation invalid"), 404
        else:
            if dao.delete(cid, cadmin):
                return jsonify(DeleteStatus="Chat with ID: " + str(cid) + " deleted."), 200

        return jsonify(Error="Invalid delete operation.")

        print("Invalid operation. Removal not allowed.")

    def deleteUserFromChat(self, cid, user_id):  # cuser1  is the admin
        dao = chatsDAO()
        row = dao.deleteUserFromChat(cid, user_id)
        print(row)
        if not row:
            return jsonify(Error="Member Not Found"), 404

        else:
            member = self.build_chats_dict(row)
            return jsonify(User=member)
