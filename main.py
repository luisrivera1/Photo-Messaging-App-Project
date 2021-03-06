from flask import Flask, jsonify, request,jsonify, request, redirect, url_for, render_template, flash
from handler.userHandler import Handler
from handler.postHandler import postHandler
from handler.statHandler import statHandler
from handler.chatHandler import chatHandler
from werkzeug.utils import secure_filename
import os


# Import Cross-Origin Resource Sharing to enable
# services on other ports on this machine or on other
# machines to access this app
from flask_cors import CORS, cross_origin

# Activate
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # This makes jsonify NOT sort automatically.
# Apply CORS to this app
CORS(app, supports_credentials=True)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'PhotoMsgApp'
app.config['UPLOAD_FOLDER'] = '/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



# UPLOAD_FOLDER = os.path.basename('static')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


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


# @app.route('/PhotoMsgApp/chats/<int:cid>/contacts/<int:contact_id>', methods=['POST'])
# def contactsOfChat(cid, contact_id):
#     if request.method == "POST":
#         return chatHandler().addContactToChat(cid, contact_id)
#     else:
#         return jsonify(Error="Method not allowed."), 405


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
        print(request.json)
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

#
# @app.route('/PhotoMsgApp/stats/<param>', methods=['GET'])
# def getAllStats(param):
#     if request.method == 'GET':
#         if not request.args:
#             if param[0].isdigit():
#                 return statHandler().getAllStats(param)
#             else:
#                 return statHandler().getAllPhotoStats(param)
#
#         else:
#             if not param[0].isdigit():
#                 return statHandler().getPhotoStatsByChoice(request.args.to_dict(), param)
#             else:
#                 return statHandler().getStatByChoice(request.args.to_dict(), param)


@app.route('/PhotoMsgApp/stats', methods=['GET'])
def getAllStatsJson():
    if request.method == 'GET':
        if not request.json:
            return statHandler().getAllStats()
        return statHandler().getStatByChoice(request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/stats/hashtags', methods=['GET'])
def getTrendingHashtags():
    if request.method == 'GET':
        return statHandler().getTrendingHashtagsTotal()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/stats/mostactivityofusers', methods=['GET'])
def getMostActivityOfUsers():
    if request.method == 'GET':
        return statHandler().getMostActivityOfUsers()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/PhotoMsgApp/stats/mostactiveusers', methods=['GET'])
def getMostActiveUsers():
    if request.method == 'GET':
        return statHandler().getMostActiveUsers()
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

@app.route('/PhotoMsgApp/post/new', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def createPost():
    if request.method == 'POST':
        if allowed_file(request.files['file'].filename):
            return postHandler().createPost(request.form, request.files['file'], app.config['UPLOAD_FOLDER'])
        return jsonify(Error="File extension not allowed"), 405
    return jsonify(Error="Method not allowed"), 405


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/PhotoMsgApp/upload', methods=['GET', 'POST'])
# def upload_file():
#     print("ENTERED THINGY")
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             print('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             print('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('upload_file', filename=filename))
#
#     return redirect(request.url)


@app.route('/PhotoMsgApp/posts/<int:pid>/dislikes/<int:uid>', methods=['POST'])
def updatePostDislikes(pid, uid):
    if request.method == 'POST':
        return postHandler().updatePostDislikes(pid, uid)
    else:
        return jsonify(Error = "Method not allowed"), 405


@app.route('/PhotoMsgApp/posts/<int:pid>/likes/<int:uid>', methods=['POST'])
def updatePostLikes(pid, uid):
    if request.method == 'POST':
        return postHandler().updatePostLikes(pid, uid)
    else:
        return jsonify(Error = "Method not allowed"), 405

@app.route('/PhotoMsgApp/chats/contacts', methods=['POST'])
def contactsOfChat():
    if request.method == "POST":
        return chatHandler().addContactToChat(request.json)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/PhotoMsgApp/stats/tophashtags', methods=['GET'])
def getTopHashtags():
    if request.method == 'GET':
        return statHandler().getTopHashtags()
    else:
        return jsonify(Error="Method not allowed."), 405


if __name__ == '__main__':
    app.run()
