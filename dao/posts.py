from Objects.Post import Post
from dao.users import usersDAO
from dao.chats import chatsDAO
from Objects.User import User
from Objects.Post import Post

class postsDAO:
    def __init__(self):
        self.posts_list = []
        firstPost = Post(1, "clopez36", "photo.jpg", "First POST!! #pollo #manzana", "02-24-2019")
        secondPost = Post(2, "ramoncin", "picture.png", "Second POST!! #manzana", "02-24-2019")
        thirdPost = Post(3, "clopez36", "newphoto.jpg", "Third Post! #nachosLoaded", "02-24-2019")
        fourthPost = Post(4, "oLaMeLlAmOlUiS", "oranges.jpg", "PRUEBAAAA! #pollo", "02-24-2019")
        fifthPost = Post(5, "ramoncin", "potato.jpg", "Que es esto? #kfc #manzana", "02-24-2019")
        sixthPost = Post(6, "clopez36", "cafe.jpg", "I am the danger  #losPollosHermanos", "02-24-2019")
        seventhPost = Post(7, "heisenberg", "pollo.png", "Los Pollos Hermanos #ElPanchoNoSeCompara", "02-24-2019")
        eighthPost = Post(8, "oLaMeLlAmOlUiS", "whatever.jpg", "No importa!", "02-24-2019")


        firstPost.addComment("Great photo!")
        firstPost.addComment("Hey!")
        for i in range(4):
            firstPost.addLike()

        firstPost.addDislike()

        for i in range(4):
            secondPost.addDislike()

        thirdPost.addComment("First comment!!!")

        seventhPost.addComment("Viva Walter!")
        seventhPost.addComment("Damn it, Skyler")

        for i in range(3):
            seventhPost.addDislike()

        seventhPost.addLike()

        print(seventhPost.getPostLikes())

        self.posts_list = [firstPost, secondPost, thirdPost, fourthPost, fifthPost, sixthPost, seventhPost, eighthPost]


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


    def postPhotoAndMsgToChat(self, cid, photo, msg):
        dao = chatsDAO()

        postToAdd = Post(4, "clopez36", photo, "new post added", msg)

        for chat in dao.getChatList():
            if chat.getId() == cid:
                chat.addPost(postToAdd)


    #Recently Added
    def getPostsFromUser(self, puser):
        result = []
        for post in self.posts_list:
            temp = []
            if post.getPostUser() == puser:
                for attribute, value in vars(post).items():
                    temp.append(value)
                    result.append(result)
                print(result)
        return result

    #Recently Added
    def getPostHashtags(self, date):
        result= []
        for post in self.posts_list:
            if post.getPostDate() == date:
                message = post.getPostMessage()
                tokens = message.split()
                for token in tokens:
                    if token[0] == "#":
                        result.append(token)

        return result

    def getPopularHashtagDict(self, date):
        hashtag_dict = {}
        print(self.getPostHashtags(date))

        for hashtag in self.getPostHashtags(date):
            print(hashtag)
            if hashtag in hashtag_dict.keys():
                hashtag_dict[hashtag] = hashtag_dict[hashtag] + 1
            else:
                hashtag_dict[hashtag] = 1

        return hashtag_dict

    def getPostPerDayDict(self):
        day_dict = {}
        print(self.posts_list)
        for post in self.posts_list:
            if post.getPostDate() in day_dict.keys():
                day_dict[post.getPostDate()] = day_dict[post.getPostDate()] + 1
            else:
                day_dict[post.getPostDate()] = 1

        print(day_dict)
        return day_dict

    def getLikesPerDayDict(self):
        likes_dict = {}
        for post in self.posts_list:
            if post.getPostDate() in likes_dict.keys():
                likes_dict[post.getPostDate()] = likes_dict[post.getPostDate()] + post.getPostLikes()
            else:
                likes_dict[post.getPostDate()] = post.getPostLikes()

        print(likes_dict)
        return likes_dict

    def getDislikesPerDayDict(self):
        dislikes_dict = {}
        for post in self.posts_list:
            if post.getPostDate() in dislikes_dict.keys():
                dislikes_dict[post.getPostDate()] = dislikes_dict[post.getPostDate()] + post.getPostDislikes()
            else:
                dislikes_dict[post.getPostDate()] = post.getPostDislikes()

        print(dislikes_dict)
        return dislikes_dict

    def getRepliesPerDayDict(self):
        replies_dict = {}
        for post in self.posts_list:
            if post.getPostDate() in replies_dict.keys():
                replies_dict[post.getPostDate()] = replies_dict[post.getPostDate()] + len(post.getPostReplies())
            else:
                replies_dict[post.getPostDate()] = len(post.getPostReplies())

        print(replies_dict)
        return replies_dict


    def getUsersDictByDay(self, date):
        users_dict = {}

        for post in self.posts_list:
            if post.getPostDate() == date:
                if post.getPostUser() in users_dict.keys():
                    users_dict[post.getPostUser()] = users_dict[post.getPostUser()] + 1
                else:
                    users_dict[post.getPostUser()] = 1

        print(users_dict)
        return users_dict

    def getUserPostsByDateDict(self, user, date):
        user_post_dict = {}

        for post in self.posts_list:
            if post.getPostDate() == date and post.getPostUser() == user:
                if post.getPostUser() in user_post_dict.keys():
                    user_post_dict[post.getPostUser()] = user_post_dict[post.getPostUser()] + 1
                else:
                    user_post_dict[post.getPostUser()] = 1

        print(user_post_dict)
        return user_post_dict

    def getPhotoRepliesDict(self, photo):
        photo_reply_dict = {}

        for post in self.posts_list:
            if post.getPostPhoto() == photo:
                photo_reply_dict[post.getPostPhoto()] = len(post.getPostReplies())

        print(photo_reply_dict)
        return photo_reply_dict

    def getPhotoLikesDict(self, photo):
        photo_likes_dict = {}

        for post in self.posts_list:
            if post.getPostPhoto() == photo:
                photo_likes_dict[post.getPostPhoto()] = post.getPostLikes()

        print(photo_likes_dict)
        return photo_likes_dict

    def getPhotoDislikesDict(self, photo):
        photo_dislikes_dict = {}

        for post in self.posts_list:
            if post.getPostPhoto() == photo:
                photo_dislikes_dict[post.getPostPhoto()] = post.getPostDislikes()

        print(photo_dislikes_dict)
        return photo_dislikes_dict


