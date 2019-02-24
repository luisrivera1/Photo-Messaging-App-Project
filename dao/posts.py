from Objects.Post import Post
from dao.users import usersDAO
from Objects.User import User

class postsDAO:
    def __init__(self):
        self.posts_list = []
        firstPost = Post(1, usersDAO.getUserById(2), "(this should be a photo)", "First POST!!", "2/24/2019", 0, 0, 0)
        # puser es un OBJECT tipo USER? o es el ID del user?.. Actualmente lo puse como USER
        secondPost = Post(2, usersDAO.getUserById(3), "(this should be a photo)", "Second POST!!", "2/24/2019", 1, 2, 0)
        self.posts_list = [firstPost, secondPost]


    def getAllPosts(self):
        result = []
        for post in self.posts_list:
            temp = []
            for attribute in post.__dict__.items():
                temp.append(attribute)
            result.append(temp)
        return result

    def getPostById(self):
        result = User

