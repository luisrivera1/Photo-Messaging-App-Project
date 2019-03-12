from flask import Flask, jsonify, request
from handler.userHandler import Handler
from handler.chatHandler import chatHandler
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
    return 'Hello, this is the parts DB App!'

@app.route('/PhotoMsgApp/users', methods=['GET', 'POST'])
def getAllUsers():
    if request.method == 'POST':
        # cambie a request.json pq el form no estaba bregando
        # parece q estaba poseido por satanas ...
        # DEBUG a ver q trae el json q manda el cliente con la nueva pieza
        print("REQUEST: ", request.json)
        return Handler().insertUser(request.json)
    else:
        if not request.args:
            return Handler().getAllUsers()
        else:
            return Handler().searchUsers(request.json)

@app.route('/PhotoMsgApp/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def getUserById(uid):
    print(uid)
    if request.method == 'GET':
        return Handler().getUserById(uid)
    elif request.method == 'PUT':
        return Handler().updateUser(uid, request.args)
    elif request.method == 'DELETE':
        return Handler().deleteUser(uid)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/PhotoMsgApp/chats', methods=['GET', 'POST'])
def getAllChats():
    if request.method == 'POST':
        # cambie a request.json pq el form no estaba bregando
        # parece q estaba poseido por satanas ...
        # DEBUG a ver q trae el json q manda el cliente con la nueva pieza
        print("REQUEST: ", request.json)
        return chatHandler().insertChat(request.json)
    else:
        if not request.args:
            return chatHandler().getAllChats()
        else:
            return chatHandler().searchChats(request.json.to_dict())



@app.route('/PhotoMsgApp/login', methods = ['GET'])
def validate_login():
    if request.method == 'GET':
        return Handler().validate_login(request.args.to_dict())


@app.route('/PhotoMsgApp/register', methods = ['PUT'])
def register_user():
    if request.method == 'PUT':
        return Handler().register_user(request.args.to_dict())

@app.route('/PhotoMsgApp/posts', methods = ['GET'])
def getAllPosts():
    if request.method == 'GET':
        return postHandler().getAllPosts()

@app.route('/PhotoMsgApp/chats/<int:cid>/posts', methods = ['GET'])
def getAllPostsFromChat(cid):
    if request.method == 'GET':
        return postHandler().getAllPostsFromChat(cid)


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

@app.route('/PhotoMsgApp/stats/<param>', methods = ['GET'])
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