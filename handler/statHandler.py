from handler import postHandler
from flask import jsonify
from operator import itemgetter

class statHandler:
    def __init__(self):
        self.post_dao = postHandler.postsDAO()

    def getMostActiveUsers(self, date):
        user_dict = self.post_dao.getUsersDictByDay(date)

        sorted_dict = sorted(user_dict.items(), key = itemgetter(1), reverse = True)

        mostActiveUsers = [sorted_dict[0][0], sorted_dict[1][0], sorted_dict[2][0]]

        return mostActiveUsers


    def getMostActiveUsers2(self,date):
        return jsonify(DateOfInterest = date, MostActiveUsers = self.getMostActiveUsers(date))

    def getRepliesPerDay(self, date):
        replies_dict = self.post_dao.getRepliesPerDayDict()

        for post_date in replies_dict.keys():
            if post_date == date:
                numOfReplies = replies_dict[date]
                return numOfReplies
        return 0

    def getRepliesPerDay2(self,date):
        return jsonify(DateOfInterest = date, RepliesPerDay=self.getRepliesPerDay(date))

    def getPostsPerDay(self, date):
        post_dict = self.post_dao.getPostPerDayDict()
        for post_date in post_dict.keys():
            if post_date == date:
                numOfPosts = post_dict[date]
                return numOfPosts

        return 0

    def getPostsPerDay2(self,date):
        return jsonify(DateOfInterest = date, PostPerDay = self.getPostsPerDay(date))


    def getLikesPerDay(self, date):
        likes_dict = self.post_dao.getLikesPerDayDict()

        for post_date in likes_dict.keys():
            if post_date == date:
                numOfLikes = likes_dict[date]
                return numOfLikes

        return None

    def getLikesPerDay2(self,date):
        return jsonify(DateOfInterest = date, LikesPerDay = self.getLikesPerDay(date))


    def getDislikesPerDay(self, date):
        dislikes_dict = self.post_dao.getDislikesPerDayDict()

        for post in dislikes_dict.keys():
            if post == date:
                numOfDislikes = dislikes_dict[date]
                return numOfDislikes

        return None

    def getDislikesPerDay2(self,date):
        return jsonify(DateOfInterest = date, DislikesPerDay = self.getDislikesPerDay(date))


    def getAllStats(self, date):
        return jsonify(DateOfInterest = date, MostActiveUsers = self.getMostActiveUsers(date), RepliesPerDay = self.getRepliesPerDay(date),
                       LikesPerDay =  self.getLikesPerDay(date), DislikesPerDay = self.getDislikesPerDay(date), PostsPerDay = self.getPostsPerDay(date))

    def getPostsPerDayByUser(self, user, date):
        user_post_dict = self.post_dao.getUserPostsByDateDict(user, date)

        for post in user_post_dict.keys():
            if post == user:
                numOfPostsByUser = user_post_dict[user]
                return numOfPostsByUser

        return 0

    def getPostsPerDayByUser2(self, user, date):
        return jsonify(DateOfInterest = date, UserOfInterest = user, PostsPerDay = self.getPostsPerDayByUser(user, date))

    def getRepliesPerPhoto(self, photo):
        photo_reply_dict = self.post_dao.getPhotoRepliesDict(photo)

        for picture in photo_reply_dict.keys():
            if picture == photo:
                numOfPhotoReplies = photo_reply_dict[photo]
                return numOfPhotoReplies

        return 0

    def getRepliesPerPhoto2(self, photo):
        return jsonify(PhotoOfInterest = photo, NumberOfReplies = self.getRepliesPerPhoto(photo))

    def getLikesPerPhoto(self, photo):
        photo_likes_dict = self.post_dao.getPhotoLikesDict(photo)

        for picture in photo_likes_dict.keys():
            if picture == photo:
                numOfPhotoLikes = photo_likes_dict[photo]
                return numOfPhotoLikes

        return None

    def getLikesPerPhoto2(self, photo):
        return jsonify(PhotoOfInterest = photo, NumberOfLikes = self.getLikesPerPhoto(photo))

    def getDislikesPerPhoto(self, photo):
        photo_dislikes_dict = self.post_dao.getPhotoDislikesDict(photo)

        for picture in photo_dislikes_dict.keys():
            if picture == photo:
                numOfPhotoDislikes = photo_dislikes_dict[photo]
                return numOfPhotoDislikes

        return None

    def getDislikesPerPhoto2(self, photo):
        return jsonify(PhotoOfInterest = photo, NumberOfDislikes = self.getDislikesPerPhoto(photo))

    def getTrendingHashtags(self, date):
        hashtag_dict = self.post_dao.getPopularHashtagDict(date)

        sorted_hashtag_dict = sorted(hashtag_dict.items(), key=itemgetter(1), reverse=True)

        return [sorted_hashtag_dict[0][0], sorted_hashtag_dict[1][0], sorted_hashtag_dict[2][0]]

    def getTrendingHashtags2(self, date):
        return jsonify(DateOfInterest = date, TrendingHashtags = self.getTrendingHashtags(date))

    def getStatByChoice(self, args, date):
        stat = args['stat']

        if len(args) == 2:
            user = args['user']

        if stat == "mostactiveusers":
            return self.getMostActiveUsers2(date)
        elif stat == "repliesperday":
            return self.getRepliesPerDay2(date)
        elif stat == "postsperday":
            return self.getPostsPerDay2(date)
        elif stat == "likesperday":
            return self.getLikesPerDay2(date)
        elif stat == "dislikesperday":
            return self.getDislikesPerDay2(date)
        elif stat == "postsperdaybyuser":
            return self.getPostsPerDayByUser2(user, date)
        elif stat == "trending":
            return self.getTrendingHashtags2(date)
        else:
            return jsonify(Error = "Invalid statistic operation"), 404


    def getPhotoStatsByChoice(self, args, photo):
        stat = args['stat']

        if stat == "replies":
            return self.getRepliesPerPhoto2(photo)
        elif stat == "likes":
            return self.getLikesPerPhoto2(photo)
        elif stat == "dislikes":
            return self.getDislikesPerPhoto2(photo)
        else:
            return jsonify(Error="Invalid statistic operation"), 404

    def getAllPhotoStats(self, photo):
        return jsonify(PhotoOfInterest = photo, NumberOfReplies = self.getRepliesPerPhoto(photo), NumberOfLikes = self.getLikesPerPhoto(photo),
                       NumberOfDislikes =  self.getDislikesPerPhoto(photo))