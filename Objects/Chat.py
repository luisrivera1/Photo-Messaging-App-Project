class Chat:

    def __init__(self, cid, cname, cmembers, cadmin):
        self.cid = cid
        self.cname = cname
        self.cmembers = cmembers
        self.cadmin = cadmin

    def getId(self):
        return self.cid

    def getName (self):
        return self.cname

    def getMembers (self):
        return self.cmembers

    def getAdmin (self):
        return self.cadmin

    


p