from flask import Flask, jsonify, request
from handler.userHandler import Handler
from handler.chatHandler import chatHandler
from handler.postHandler import postHandler

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
            return Handler().searchUsers(request.args.to_dict())


@app.route('/PhotoMsgApp/chats', methods=['GET', 'PUT', 'POST', 'DELETE'])
def getAllChats():
    if request.method == 'GET':
        if not request.args:
            return chatHandler().getAllChats()
        else:
            return chatHandler().searchChats(request.args.to_dict())
    elif request.method == 'PUT':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        return chatHandler().deleteChat(request.args.to_dict())


@app.route('/PhotoMsgApp/login', methods=['GET'])
def validate_login():
    if request.method == 'GET':
        return Handler().validate_login(request.args.to_dict())


@app.route('/PhotoMsgApp/register', methods=['PUT'])
def register_user():
    if request.method == 'PUT':
        return Handler().register_user(request.args.to_dict())


@app.route('/PhotoMsgApp/posts', methods=['GET'])
def getAllPosts():
    if request.method == 'GET':
        return postHandler().getAllPosts()


@app.route('/PhotoMsgApp/chats/<int:cid>/posts', methods=['GET'])
def getAllPostsFromChat(cid):
    if request.method == 'GET':
        return postHandler().getAllPostsFromChat(cid)

@app.route('/PhotoMsgApp/users/<int:uid>/Contacts', methods=['GET', 'PUT', 'DELETE'])
def getContactById(uid):
    print(uid)
    if request.method == 'GET':
        return Handler().getContactsById(uid)
    elif request.method == 'PUT':
        return Handler().updateContactList(uid, request.json)
    elif request.method == 'DELETE':  # NOT YET!!!
        return Handler().deleteContact(uid, request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


if __name__ == '__main__':
    app.run()