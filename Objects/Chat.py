class Chat:

    def __init__(self,cid, cname, cmembers,cadmin):
        self.cid = cid
        self.cname = cname
        self.cmembers = cmembers
        self.cadmin = cadmin

    def getcId(self):
        return self.cid

    def getcName (self):
        return self.name

    def getcMembers (self):
        return self.members

    def getcAdmin(self):
        return self.cadmin

    


