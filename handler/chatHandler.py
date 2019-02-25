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
            result = self.build_c_chats(row)
            result_list.append(result)
        return jsonify(Chats=result_list)


    def getChatsById(self, cid):
        dao = chatsDAO()
        row = dao.getChatById(cid)
        if not row:
            return jsonify(Error="Chat Not Found"), 404
        else:
            chats = self.build_chats_dict(row)
            return jsonify(Chats=chats)

    def searchChats(self, args):
        cname = args.get("cname")

        dao = chatsDAO()
        chats_list = []
        if (len(args) == 1) and cname:
            chats_list = dao.getChatsByName(cname)

        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in chats_list:
            result = self.build_chats_dict(row)
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

                if cid and cname and cmembers and cadmin :
                    dao = chatsDAO()
                    cid = dao.insert(cid, cname, cmembers, cadmin)
                    result = self.build_user_attributes(cid, cname, cmembers, cadmin)
                    return jsonify(Chat=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in post request"), 400

    def insertChatJson(self, json):
        cid= json['cid']
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


    def deleteChat(self, cid):
        dao = chatsDAO()
        if not dao.getChatById(cid):
            return jsonify(Error="Post not found."), 404
        else:
            dao.delete(cid)
            return jsonify(DeleteStatus="OK"), 200


    def deleteUserFromChat(self, cuser1, cuser2, cid): # cuser1  is the admin
        dao = chatsDAO()
        for chat in chatsDAO.getChatList():
            if chat.getId() == cid:
                if cuser1 in chat and cuser2 in chat:
                      #valid operation
                    if cuser1 == chat.getAdmin() and cuser2 != cuser1:
                        dao.deleteUserFromChat(chat, cuser2)
                        break

        print("Invalid operation. Removal not allowed.")


