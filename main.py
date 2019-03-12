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
            return chatHandler().searchChats(request.json)



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

@app.route('/PhotoMsgApp/stats/<date>', methods = ['GET'])
def getAllStats(date):
    if request.method == 'GET':
        if not request.args:
            return statHandler().getAllStats(date)
        else:
            return statHandler().getStatByChoice(request.args.to_dict(), date)








#
# @app.route('/PartApp/parts/<int:pid>/suppliers')
# def getSuppliersByPartId(pid):
#     return PartHandler().getSuppliersByPartId(pid)
#
# @app.route('/PartApp/suppliers', methods=['GET', 'POST'])
# def getAllSuppliers():
#     if request.method == 'POST':
#         return SupplierHandler().insertSupplier(request.form)
#     else :
#         if not request.args:
#             return SupplierHandler().getAllSuppliers()
#         else:
#             return SupplierHandler().searchSuppliers(request.args)
#
# @app.route('/PartApp/suppliers/<int:sid>',
#            methods=['GET', 'PUT', 'DELETE'])
# def getSupplierById(sid):
#     if request.method == 'GET':
#         return SupplierHandler().getSupplierById(sid)
#     elif request.method == 'PUT':
#         pass
#     elif request.method == 'DELETE':
#         pass
#     else:
#         return jsonify(Error = "Method not allowed"), 405
#
#
# @app.route('/PartApp/suppliers/<int:sid>/parts')
# def getPartsBySuplierId(sid):
#     return SupplierHandler().getPartsBySupplierId(sid)
#
# @app.route('/PartApp/parts/countbypartid')
# def getCountByPartId():
#     return PartHandler().getCountByPartId()

if __name__ == '__main__':
    app.run()