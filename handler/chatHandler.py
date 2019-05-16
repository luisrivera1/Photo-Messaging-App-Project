from flask import jsonify
from dao.chats import chatsDAO
from dao.users import usersDAO


class chatHandler:
    def build_chats_dict(self, row):
        result = {}
        result['cid'] = row[0]
        result['cname'] = row[1]
        result['cadmin'] = row[2]

        return result

    def build_chats_attributes(self, cid, cname, cadmin):
        result = {}
        result['cid'] = cid
        result['cname'] = cname
        result['cadmin'] = cadmin

        return result

    def build_users_from_chat_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['ufirstname'] = row[1]
        result['ulastname'] = row[2]

        return result

    def build_posts_from_chat_dict(self, row):
        result = {}
        result['pid'] = row[0]
        result['pmessage'] = row[1]
        result['puser'] = row[2]

        return result

    def build_contact_attributes(self, ufirstname, ulastname, uemail):
        result = {}
        result['ufirstname'] = ufirstname
        result['ulastname'] = ulastname
        result['uemail'] = uemail
        return result

    def getAllChats(self):
        dao = chatsDAO()
        chats_list = dao.getAllChats()
        result_list = []

        print(chats_list)
        for row in chats_list:
            print(row)
            result = self.build_chats_dict(row)
            result_list.append(result)
        return jsonify(Chats=result_list)

    def getAllChatsOfUser(self, uid):
        dao2 = usersDAO()
        if not dao2.getUserById(uid):
            return jsonify(Error="User " + str(uid) + " not found"), 404
        dao = chatsDAO()
        chat_list = dao.getAllChatsOfUser(uid)
        if not chat_list:
            return jsonify(NoChats="User " + str(uid) + " is not a member of any chat."), 404
        result_list = []
        for row in chat_list:
            print(row)
            result = self.build_chats_dict(row)
            result_list.append(result)
        return jsonify(Chats=result_list)

    def getChatsById(self, cid):
        dao = chatsDAO()
        row = dao.getChatById(cid)
        if not row:
            return jsonify(Error="Chat Not Found"), 404
        else:
            chat = self.build_chats_dict(row)
            return jsonify(Chats=chat)

    def getChatsByChatname(self, form):
        dao = chatsDAO()
        cname = form['cname']
        cid = dao.getChatByChatName(cname)
        if not cid:
            return jsonify(Error="Chat Not Found"), 404
        else:
            # chats = self.build_chats_dict(row)
            return jsonify(Chat={"cid":cid})

    def getChatMemberByID(self, chat_id, mem_id):
        dao = chatsDAO()
        row = dao.getChatMemberById(chat_id, mem_id)
        if not row:
            return jsonify(Error="Member Not Found"), 404

        else:
            member = self.build_chats_dict(row)
            return jsonify(User = member)

    def searchChats(self, args):
        cname = args["cname"]

        dao = chatsDAO()

        if (len(args) == 1) and cname:
            chats_list = dao.getChatByChatName(cname)

        else:
            return jsonify(Error = "Malformed query string"), 400

        print(chats_list)
        result_list = self.build_chats_dict(chats_list)
        return jsonify(Chats=result_list)

    # def insertChatJson(self, json):
    #     cid= json['cid']
    #     cname = json['cname']
    #     cadmin = json['cadmin']
    #     if cid and cname and cadmin:
    #         dao = chatsDAO()
    #         cid = dao.insert(cid, cname, cadmin)
    #         result = self.build_chats_attributes(cid, cname, cadmin)
    #         return jsonify(Chat=result), 201
    #     else:
    #         return jsonify(Error="Unexpected attributes in post request"), 400

    def createChat(self, form):
            print("form: ", form)
            if len(form) != 2:
                return jsonify(Error="Malformed create chat request"), 400
            else:
                try:
                    cname = form['cname']
                    cadmin = form['cadmin']

                    if cname and cadmin:
                        dao = chatsDAO()
                        cid = dao.createChat(cname, cadmin)

                        result = self.build_chats_attributes(cid, cname, cadmin)
                        return jsonify(Chat=result), 200
                    else:
                        return jsonify(Error="Unexpected attributes in create chat request"), 400
                except:
                    return jsonify(Error="Unexpected attributes in create chat request"), 400

    def deleteChat(self, form):
        if len(form) != 2:
            return jsonify(Error="Malformed delete chat request"), 400

        try:
            cid = form['cid']
            uid = form['uid']
        except:
            return jsonify(Error="Unexpected attributes in delete chat request"), 400
        dao = chatsDAO()
        if not dao.getChatById(cid):
            return jsonify(Error="Chat not found."), 404
        else:
            if not dao.isAdmin(cid, uid):
                return jsonify(Error="User " + str(uid) + " is not admin of chat " + str(cid)), 405
            else:
                if dao.deleteMembersOfChat(cid, dao.getChatMembers(cid)) and dao.deleteChat(cid) == 1:
                    return jsonify(DeletedChat="Chat " + str(cid) + " deleted."), 200
                else:
                    return jsonify(Error="Delete chat was unsuccessful"), 400

    def deleteUserFromChat(self, cid, admin_id, uid):
        dao = chatsDAO()
        dao2 = usersDAO()
        if not dao.getChatById(cid):
            return jsonify(Error="Chat with id: " + str(cid) + " not found."), 404
        if not dao2.getUserById(uid):
            return jsonify(Error="User with id: " + str(uid) + " not found."), 404
        if not dao.isMember(cid, uid):
            return jsonify(Error="User with id: " + str(uid) + " is not a member of chat with id: " + str(cid))
        if not dao.isAdmin(cid, admin_id):
            return jsonify(Error="You are not admin")
        if admin_id == uid:
            return jsonify(Error="You cannot remove yourself from the chat.")
        if dao.deleteUserFromChat(cid, uid) == 1:
            return jsonify(DeletedChatMember="User: " + str(uid) + " from Chat " + str(cid) + " was deleted."), 200
        else:
            return jsonify(Error="Delete user: " + str(uid) + " from chat: " + str(cid) + " was unsuccessful"), 400

    # def deleteUserFromChat(self, cuser1, cuser2, cid): # cuser1  is the admin
    #     dao = chatsDAO()
    #     for chat in chatsDAO.getChatList():
    #         if chat.getId() == cid:
    #             if cuser1 in chat and cuser2 in chat:
    #                   #valid operation
    #                 if cuser1 == chat.getAdmin() and cuser2 != cuser1:
    #                     dao.deleteUserFromChat(chat, cuser2)
    #                     return jsonify(DeleteStatus="OK"), 200
    #                     break
    #
    #             else:
    #                 return jsonify(Error="User Not Found"), 404
    #     print("Invalid operation. Removal not allowed.")

    def addContactToChat(self, cid, contact_id):
        dao = chatsDAO()
        dao2 = usersDAO()
        if not dao.getChatById(cid):
            return jsonify(Error="Chat with id: " + str(cid) + " not found."), 404
        if not dao2.getUserById(contact_id):
            return jsonify(Error="User with contact id: " + str(contact_id) + " not found."), 404
        if dao.isMember(cid, contact_id):
            return jsonify(Error="User with contact id: " + str(contact_id) + " is already a member of chat with id: " + str(cid))
        if dao.addMemberToChat(cid, contact_id) == 1:
            return jsonify(AddedChatMember="User with contact id: " + str(contact_id) + " was added to Chat: " + str(cid)), 200
        else:
            return jsonify(Error="Adding contact with id: " + str(contact_id) + " to chat: " + str(cid) + " was unsuccessful"), 400

    def addContactToChatJson(self, cid, form):
        print(cid)
        dao = chatsDAO()
        dao2 = usersDAO()
        if not dao.getChatById(cid):
            return jsonify(Error="Chat with id:" + str(cid) + " not found."), 404
        if len(form) != 3:
            return jsonify(Error="Malformed add contact to chat request"), 400
        ufirstname = form['ufirstname']
        ulastname = form['ulastname']
        uemail = form['uemail']
        if ufirstname and ulastname and uemail:
            row = dao2.getUserByEmail(uemail)
            if not row:
                return jsonify(Error="User with email: " + str(uemail) + " not found."), 404
            uid = row[0]
            if dao.isMember(cid, uid):
                return jsonify(Error="User with email: " + str(uemail) + " is already a member of chat with id: " + str(cid))
            if dao.addMemberToChat(cid, uid) == 1:
                result = self.build_contact_attributes(ufirstname, ulastname, uemail)
                return jsonify(AddedContactToChat=result), 200
        else:
            return jsonify(Error="Unexpected attributes in add contact to chat request"), 400

    def addPostToChat(self, args, form):
        cid = int(args['cid'])
        dao = chatsDAO()
        if not dao.getChatById(cid):
            return jsonify(Error="Chat not found."), 404
        else:
            pid = form['pid']
            puser = form['puser']
            pphoto = form['pphoto']
            pmessage = form['pmessage']
            pdate = form['pdate']
            plike = form['plike']
            pdislikes = form['pdislikes']
            if pid and puser and pphoto and pmessage and pdate and plike and pdislikes:
                return jsonify(AddStatus="OK"), 200
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400

    # def removeUserFromChat(self, cid, args):
    #     dao = chatsDAO()
    #     udao = userDAO()
    #
    #     uid = args['uid']
    #
    #     if not dao.getChatById(cid) or dao.get:
    #         return jsonify(Error = "Chat not found"), 404
    #
    #     else:
    #

    def getAllUsersFromChat(self, cid):
        dao = chatsDAO()
        if not dao.getChatById(cid):
            return jsonify(Error="Chat not found."), 404
        else:
            users_list = dao.getAllUsersFromChat(cid)
            result_list = []
            for row in users_list:
                result = self.build_users_from_chat_dict(row)
                result_list.append(result)
            return jsonify(UsersInChat=result_list)

    def getAdminOfChat(self, cid):
        dao = chatsDAO()
        if not dao.getChatById(cid):
            return jsonify(Error="Chat not found."), 404
        else:
            row = dao.getAdminOfChat(cid)
            result = self.build_users_from_chat_dict(row)
            return jsonify(AdminFromChat=result)

    def getAllPostsFromChat(self, cid):
        dao = chatsDAO()
        if not dao.getChatById(cid):
            return jsonify(Error="Chat not found."), 404
        else:
            posts_list = dao.getAllPostsFromChat(cid)
            result_list = []
            for row in posts_list:
                print(posts_list)
                result = self.build_posts_from_chat_dict(row)
                result_list.append(result)
            return jsonify(UsersInChat=result_list)

    def getUsersForAdding(self, cid, uid):
        dao = chatsDAO()
        udao = usersDAO()

        if not dao.getChatById(cid):
            return jsonify(Error = "Chat not found."), 404

        elif not udao.getUserById(uid):
            return jsonify(Error = "User not found."), 404

        else:
            chat_members = dao.getAllUsersFromChat(cid)

            if len(chat_members) == 1:
                return jsonify(Error = "Only user in chat is admin.")

            contact_list = udao.getContactListFromUserId(uid)

            print(chat_members)
            print(contact_list)

            contacts = []

            for contact in contact_list:
                if not contact in chat_members:
                    contacts.append(contact)

            print(contacts)

            if len(contacts) > 0:
                result = []

                for row in contacts:
                    result.append(self.build_users_from_chat_dict(row))

                    print(result)

                return jsonify(Contacts = result), 200

            else:
                return jsonify(Error = "All users in contact list already in chat.")





