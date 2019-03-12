from dao.users import usersDAO

class Chat:
    def __init__(self, cid, cname, cadmin):
        dao = usersDAO()

        self.cid = cid
        self.cname = cname
        self.cmembers = []

        self.cmembers.append(dao.getUsersByUsernamev2(cadmin))

        self.postlist = []

        self.cadmin = cadmin

    def getId(self):
        return self.cid

    def getName(self):
        return self.cname

    def getMembers(self):
        return self.cmembers

    def addToChatMembers(self, member):
        self.cmembers.append(member)

    def removeChatMember(self, member):
        self.cmembers.remove(member)

    def getAdmin(self):
        return self.cadmin

    def getPosts(self):
        return self.postlist

    def addPost(self, post):
        temp = []
        for attribute, value in vars(post).items():
            temp.append(value)
        self.postlist.append(temp)
    


