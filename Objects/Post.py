class Post:

    def __init__(self, pid, puser, pphoto, pmessage, pdate, plikes, pdislikes, preplies):
        self.pid = pid
        self.puser = puser
        self.pphoto = pphoto
        self.pmessage = pmessage
        self.pdate = pdate
        self.plikes = plikes
        self.pdislikes = pdislikes
        self.preplies = preplies

    def getId (self):
        return self.pid

    def getPostUser(self):
        return self.puser

    def getPostPhoto(self):
        return self.pphoto

    def getPostMessage(self):
        return self.pmessage

    def getPostDate(self):
        return self.pdate

    def getPostLikes(self):
        return self.plikes

    def getPostDislikes(self):
        return self.pdislikes

    def getPostReplies(self):
        return self.preplies



