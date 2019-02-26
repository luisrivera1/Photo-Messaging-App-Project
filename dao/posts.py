from Objects.Post import Post

class postsDAO:
    def __init__(self):
        self.posts_list = []
        firstPost = Post(1, "clopez36", "photo.jpg", "First POST!!", "2/24/2019")
        secondPost = Post(2, " ramoncin", "picture.png", "Second POST!!", "2/25/2019")
        self.posts_list = [firstPost, secondPost]


    def getAllPosts(self):
        result = []
        for post in self.posts_list:
            temp = []
            for attribute, value in vars(post).items():
                temp.append(value)
            result.append(temp)
        return result

    def getPostById(self, pid):
        result = []
        for post in self.posts_list:
            if post.getId() == pid:
                for attribute, value in vars(post).items():
                    result.append(value)
        return result






