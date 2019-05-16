from flask import Flask, jsonify, request
from handler.userHandler import Handler
from handler.postHandler import postHandler
from handler.statHandler import statHandler
from handler.chatHandler import chatHandler


# Import Cross-Origin Resource Sharing to enable
# services on other ports on this machine or on other
# machines to access this app
from flask_cors import CORS, cross_origin

# Activate
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # This makes jsonify NOT sort automatically.
app.config['CORS_HEADERS'] = 'Content-Type'
# Apply CORS to this app
CORS(app, supports_credentials = True)


@app.route('/PhotoMsgApp/users', methods=['GET', 'POST'])
def getAllUsers():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return Handler().insertUser(request.json)
    else:
        if not request.args:
            return Handler().getAllUsers()
        else:
            return Handler().getUserByIdORUsername(request.args)
            # return Handler().searchUsers(request.args.to_dict())  # Is this even necessary?


@app.route('/PhotoMsgApp/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def getUserById(uid):
    print(uid)
    if request.method == 'GET':
        return Handler().getUserById(uid)
    elif request.method == 'PUT':
        return Handler().updateUser(uid, request.json)  # update needs to be implemented
    elif request.method == 'DELETE':
        return Handler().deleteUser(uid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/users/<int:uid>/chats', methods=['GET'])
def getAllChatsOfUser(uid):
    print(uid)
    if request.method == 'GET':
        return chatHandler().getAllChatsOfUser(uid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/users/<int:uid>/contacts', methods=['GET', 'POST', 'DELETE'])
def getAllContactsFromUser(uid):
    if request.method == 'GET':
        return Handler().getContactsById(uid)
    elif request.method == 'POST':
        return Handler().addToContactList(uid, request.json)
    elif request.method == 'DELETE':
        if not request.json:
            return jsonify(Error="Need to specify parameters for deletion"), 405
        else:
            return Handler().deleteContact(uid, request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/users/<int:uid>/contacts/<int:cid>', methods=['DELETE'])
def deleteContactFromUser(uid, cid):
    if request.method == 'DELETE':
        form = {}
        form['cid'] = cid
        return Handler().deleteContact(uid, (form))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/chats', methods=['GET', 'POST', 'DELETE'])
def getAllChats():
    # if request.method == 'POST':
    #     if not request.args:
    #         # cambie a request.json pq el form no estaba bregando
    #         # parece q estaba poseido por satanas ...
    #         # DEBUG a ver q trae el json q manda el cliente con la nueva pieza
    #         print("REQUEST: ", request.json)
    #         return chatHandler().insertChat(request.json)
    #     else:
    #         return chatHandler().addPostToChat(request.args.to_dict(), request.json)
    if request.method == "GET":
        if not request.args:
            return chatHandler().getAllChats()
        else:
            return chatHandler().getChatsByChatname(request.args)
    elif request.method == "POST":
        if not request.json:
            return jsonify(Error="Need to specify parameters for chat creation"), 405
        return chatHandler().createChat(request.json)
    elif request.method == "DELETE":
        return chatHandler().deleteChat(request.args)


@app.route('/PhotoMsgApp/chats/<int:cid>/users', methods=['GET'])
def usersOfChat(cid):
    print(cid)
    if request.method == "GET":
        return chatHandler().getAllUsersFromChat(cid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/chats/<int:cid>/user/<int:admin_id>/delete/<int:uid>', methods=['DELETE'])
def deleteMemberOfChat(cid, admin_id, uid):
    if request.method == "DELETE":
        return chatHandler().deleteUserFromChat(cid, admin_id, uid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/chats/contacts/', methods=['POST', 'OPTIONS', 'PUT'])
@cross_origin(origin = '*', headers = ['Content-Type','Access-Control-Allow-Origin', 'Access-Control-Allow-Method', 'Access-Control-Allow-Headers'])

def contactsOfChat(cid, contact_id):
    print(cid, contact_id)
    if request.method == "POST":
        return chatHandler().addContactToChat(request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/chats/<int:cid>/contacts', methods=['POST'])
def contactsOfChatJson(cid):
    if request.method == "POST":
        return chatHandler().addContactToChatJson(cid, request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/chats/<int:cid>/admin', methods=['GET'])
def adminOfChat(cid):
    print(cid)
    if request.method == "GET":
        return chatHandler().getAdminOfChat(cid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/chats/<int:cid>/posts', methods=['GET'])
def PostsOfChat(cid):
    print(cid)
    if request.method == "GET":
        return chatHandler().getAllPostsFromChat(cid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/posts/<int:pid>/users/dislikes', methods=['GET'])
def usersWhodislikedPost(pid):
    print(pid)
    if request.method == "GET":
        return postHandler().getUsersWhoDislikedPost(pid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/posts/<int:pid>/users/likes', methods=['GET'])
def usersWholikedPost(pid):
    print(pid)
    if request.method == "GET":
        return postHandler().getUsersWhoLikedPost(pid)
    else:
        return jsonify(Error="Method not allowed."), 405

# @app.route('/PhotoMsgApp/chats/<int:cid>', methods=['POST', 'DELETE'])
# def modifyContacts(cid):
#     print(cid)
#     if request.method == "POST":
#         return chatHandler().addContactToChat(cid, request.json)
#     elif request.method == "DELETE":
#         if not request.args:
#             return "Invalid operation!"
#         else:
#             return chatHandler().deleteUserFromChat(cid, request.args.to_dict())


@app.route('/PhotoMsgApp/posts', methods=['GET', 'POST'])
def getAllPosts():
    if request.method == 'GET':
        if not request.args:
            return postHandler().getAllPosts()
        # else:
        #     return postHandler().getPostById(request.args.to_dict())
    # http://127.0.0.1:5000/PhotoMsgApp/posts?pid=1&operation=dislike
    if request.method == 'POST':
        return postHandler().insertPost(request.json)

    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/posts/<int:pid>', methods=['GET', 'DELETE'])
def getASinglePost(pid):
    if request.method == 'GET':
        return postHandler().getPostById(pid)
    if request.method == 'DELETE':
        return postHandler().deletePost(pid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/posts/<int:pid>/likes', methods=['GET'])
def getLikesOfAPost(pid):
    if request.method == 'GET':
        return postHandler().getLikesOfAPost(pid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/posts/<int:pid>/dislikes', methods=['GET'])
def getDislikesOfAPost(pid):
    if request.method == 'GET':
        return postHandler().getDisikesOfAPost(pid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/posts/<int:pid>/replies', methods=['GET'])
def getRepliesOfAPost(pid):
    if request.method == 'GET':
        return postHandler().getRepliesOfAPost(pid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/posts/reply', methods=['PUT'])
def updatePostReplies():
    if request.method == 'PUT':
        return postHandler().updatePostReplies(request.json)


#  http://127.0.0.1:5000/PhotoMsgApp/postsFromChat?cid=1
@app.route('/PhotoMsgApp/postsFromChat', methods=['GET'])
def getAllPostsFromChat():
    if request.method == 'GET':
        # "You need to specify the CHAT ID from which to GET posts."
        return postHandler().getAllPostsFromChat(request.args.to_dict())


@app.route('/PhotoMsgApp/login', methods=['POST'])
def validate_login():
    if request.method == 'POST':
        print(request.json)
        print(Handler().validate_login(request.json))
        return Handler().validate_login(request.json)


@app.route('/PhotoMsgApp/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        return Handler().insertUser(request.json)


#  http://127.0.0.1:5000/PhotoMsgApp/contacts?uid=2
@app.route('/PhotoMsgApp/contacts', methods=['GET', 'POST', 'DELETE'])
def getContactById():
    if request.method == 'GET':
        return Handler().getContactsById(request.args.to_dict())
    elif request.method == 'POST':
        return Handler().addToContactList(request.args.to_dict(), request.json)
    elif request.method == 'DELETE':  # NOT YET!!!
        return Handler().deleteContact(request.args.to_dict(), request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


'''
La ruta tiene dos opciones:
  Si el parametro es una fecha(con el formato MM-DD-YYYY),
  existe la posibilidad para ver todas las estadisticas
  asociadas a dicha fecha, o el poder ver una estadistica en
  particular.
  
  Ejemplo: /PhotoMsgApp/stats/02-24-2019 (Todas las estadisticas)
           /PhotoMsgApp/stats/02-24-2019?likesperday (Estadistica especifica)
           
  Segunda alternativa es que el parametro sea un string representando una foto.
  Dicho parametro sirve para devolver las estadisticas de la foto pertinente.
  
  Ejemplo: /PhotoMsgApp/stats/pollo.png (Todas las estadisticas)
           /PhotoMsgApp/stats/pollo.png?stat=likes (Estadistica especifica)
'''


@app.route('/PhotoMsgApp/stats/<param>', methods=['GET'])
def getAllStats(param):
    if request.method == 'GET':
        if not request.args:
            if param[0].isdigit():
                return statHandler().getAllStats(param)
            else:
                return statHandler().getAllPhotoStats(param)

        else:
            if not param[0].isdigit():
                return statHandler().getPhotoStatsByChoice(request.args.to_dict(), param)
            else:
                return statHandler().getStatByChoice(request.args.to_dict(), param)


@app.route('/PhotoMsgApp/stats', methods=['GET'])
def getAllStatsJson():
    if request.method == 'GET':
        if not request.json:
            return statHandler().getAllStats()
        return statHandler().getStatByChoice(request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/posts/<int:pid>/reply', methods=['POST'])
def replyToPost(pid):
    print(pid)
    print(request.json)
    if request.method == 'POST':
        return postHandler().addReplyToPost(pid, request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/uid', methods = ['GET'])
def getIdByUsername():
    print(request.args)
    if request.method == "GET":
        print(Handler().getIdByUsername(request.args).data)
        return Handler().getIdByUsername(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/posts/chat', methods=["GET"])
def getAllPostsFromChatname():
    if request.method == "GET":
        return postHandler().getAllPostsFromChatname(request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/posts/chat/original', methods= ["GET"])
def getAllOriginalPostsFromChat():
    if request.method == "GET":
        return postHandler().getAllOriginalPostsFromChat(request.args)
    else:
        return jsonify(Error = "Method not allowed"), 405


@app.route('/PhotoMsgApp/chats/<int:cid>/contactlist/<int:uid>', methods = ["GET"])
def getValidUsersToAddToChat(cid, uid):
    if request.method == "GET":
        return chatHandler().getUsersForAdding(cid, uid)
    else:
        return jsonify(Error = "Method not allowed"), 405


@app.route('/PhotoMsgApp/posts/<int:pid>/dislikes/<int:uid>', methods=['PUT'])
def updatePostDislikes(pid, uid):
    if request.method == 'PUT':
        return postHandler().updatePostDislikes(pid, uid)
    else:
        return jsonify(Error = "Method not allowed"), 405


if __name__ == '__main__':
    app.run()
