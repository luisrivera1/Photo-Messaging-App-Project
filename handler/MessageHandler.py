from dao.MessageDAO import MessageDAO
from flask import jsonify
from dao.HashtagDAO import HashtagDao

class MessageHandler:

    def maptoDicMessage(self, m):
        mapped = {'MessageId': m[0], 'Message': m[1], 'Chat': m[2], 'Date': m[3], 'Time': m[4], 'SenderId': m[5]}
        return mapped

    def getAllMessages(self):
        messages = MessageDAO().allMessages()
        if messages == None:
            return jsonify(Error="NOT FOUND"), 404
        result = []
        for m in messages:
            result.append(self.maptoDicMessage(m))
        return jsonify(AllMessages=result)

    def getMessagesFromChat(self, cid):
        messages = MessageDAO().messagesFromChat(cid)
        if messages == None:
            return jsonify(Error="NOT FOUND"), 404
        result = []
        for m in messages:
            result.append(self.maptoDicMessage(m))
        return jsonify(MessagesFromChat=result)

    def getMessagesFromUser(self, uid):
        messages = MessageDAO().messagesFromUser(uid)
        if messages == None:
            return jsonify(Error="NOT FOUND"), 404
        result = []
        for m in messages:
            result.append(self.maptoDicMessage(m))
        return jsonify(MessagesFromUser=result)

    def getMessageReplies(self, mid):
        messages = MessageDAO().messageReply(mid)
        if messages == None:
            return jsonify(Error="NOT FOUND"), 404
        result = []
        for m in messages:
            result.append(self.maptoDicMessage(m))
        return jsonify(MessageReplies=result)
    
    def getalllikes(self):
        dao = MessageDAO().getLikes()
        if dao == None:
            return jsonify(Error="NOT FOUND"), 404
        result = []
        for l in dao:
            result.append(self.maplikes(l))
        return jsonify(AllLikes=result)

    def getalldislikes(self):
        dao = MessageDAO().getDislikes()
        if dao == None:
            return jsonify(Error="NOT FOUND"), 404
        result = []
        for l in dao:
            result.append(self.mapdislikes(l))
        return jsonify(AllDislikes=result)

    def getmessagedislikes(self, mid):
        dao = MessageDAO().messagesDislikes(mid)
        if dao == None:
            return jsonify(Error="NOT FOUND"), 404
        result = []
        for l in dao:
            result.append(self.mapdislikes(l))
        return jsonify(LikeInMessage=result)

    def getmessagelikes(self, mid):
        dao = MessageDAO().messageLikes(mid)
        if dao == None:
            return jsonify(Error="NOT FOUND"), 404
        result = []
        for l in dao:
            result.append(self.maplikes(l))
        return jsonify(DislikesInMessage=result)

    def mapdislikes(self, d):
        return {'dislikeid': d[0], 'messagesDisliked': d[1], 'userThatDisliked': d[2]}

    def maplikes(self, d):
        return {'likeid': d[0], 'messagesLiked': d[1], 'userThatLiked': d[2]}

    def mapNumdislike(self, d):
        return{'Number of Dislikes': d}
    
    def mapNumlike(self, d):
        return{'Number of Likes': d}

