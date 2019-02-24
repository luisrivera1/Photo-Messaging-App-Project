class Chat:

    def __init__(self, cname, cmembers, cadmin):
        self.cname = cname
        self.cmembers = cmembers
        self.cadmin = cadmin

    def getName (self):
        return self.cname

    def getMembers (self):
        return self.cmembers

    def getAdmin (self):
        return self.cadmin

    


