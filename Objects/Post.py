class Post:

    def __init__(self, pid, puser, pphoto, pmessage, pdate):
        self.pid = pid
        self.puser = puser
        self.pphoto = pphoto
        self.pmessage = pmessage
        self.pdate = pdate
        self.plikes = 0
        self.pdislikes = 0
        self.preplies = []


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

    def addLike(self):
        self.plikes = self.plikes + 1

    def addDislike(self):
        self.pdislikes = self.pdislikes + 1

    def addComment(self, comment):
        self.preplies.append(comment)



