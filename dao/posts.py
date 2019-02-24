from Objects.Post import Post
from dao.users import usersDAO
from Objects.User import User

class postsDAO:
    def __init__(self):
        self.posts_list = []
        firstPost = Post(1, usersDAO.)