from flask import Flask, jsonify, request
from handler.userHandler import Handler
from handler.postHandler import postHandler
from handler.statHandler import statHandler

from handler.supplier import SupplierHandler
from handler.chatHandler import chatHandler
from Objects.Chat import Chat
from Objects.User import User


# Import Cross-Origin Resource Sharing to enable
# services on other ports on this machine or on other
# machines to access this app
from flask_cors import CORS, cross_origin

# Activate
app = Flask(__name__)
# Apply CORS to this app
CORS(app)


@app.route('/')
def greeting():
    return 'Hello, this is the InstaWHAT DB App!'


@app.route('/PhotoMsgApp/users', methods=['GET', 'POST'])
def getAllUsers():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return Handler().insertUser(request.json)
    else:
        if not request.args:
            return Handler().getAllUsers()
        else:
            return Handler().searchUsers(request.args.to_dict())  # Is this even necessary?


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


@app.route('/PhotoMsgApp/chats', methods=['GET', 'POST', 'DELETE'])
def getAllChats():
    if request.method == 'POST':
        if not request.args:
            # cambie a request.json pq el form no estaba bregando
            # parece q estaba poseido por satanas ...
            # DEBUG a ver q trae el json q manda el cliente con la nueva pieza
            print("REQUEST: ", request.json)
            return chatHandler().insertChat(request.json)
        else:
            return chatHandler().addPostToChat(request.args.to_dict(), request.json)
    elif request.method == "GET":
        if not request.args:
            return chatHandler().getAllChats()
        else:
            return chatHandler().searchChats(request.args.to_dict())

    elif request.method == "DELETE":
        return chatHandler().deleteChat(request.args.to_dict())


@app.route('/PhotoMsgApp/chats/<int:cid>', methods=['POST', 'DELETE'])
def modifyContacts(cid):
    print(cid)
    if request.method == "POST":
        return chatHandler().addContactToChat(cid, request.json)
    elif request.method == "DELETE":
        if not request.args:
            return "Invalid operation!"
        else:
            return chatHandler().deleteUserFromChat(cid, request.args.to_dict())


@app.route('/PhotoMsgApp/login', methods=['GET'])
def validate_login():
    if request.method == 'GET':
        return Handler().validate_login(request.json)


@app.route('/PhotoMsgApp/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        return Handler().register_user(request.json)


@app.route('/PhotoMsgApp/posts', methods=['GET', 'PUT'])
def getAllPosts():
    if request.method == 'GET':
        if not request.args:
            return postHandler().getAllPosts()
        else:
            return postHandler().getPostById(request.args.to_dict())
    # http://127.0.0.1:5000/PhotoMsgApp/posts?pid=1&operation=dislike
    if request.method == 'PUT':
        return postHandler().updateLikeDislike(request.args.to_dict())


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


if __name__ == '__main__':
    app.run()
