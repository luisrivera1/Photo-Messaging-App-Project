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

    def getRepliesPerDay2(self,date):
        return jsonify(DateOfInterest = date, RepliesPerDay=self.getRepliesPerDay(date))

    def getPostsPerDay(self, date):
        post_dict = self.post_dao.getPostPerDayDict()
        for post_date in post_dict.keys():
            if post_date == date:
                numOfPosts = post_dict[date]

        return numOfPosts

    def getPostsPerDay2(self,date):
        return jsonify(DateOfInterest = date, PostPerDay = self.getPostsPerDay(date))


    def getLikesPerDay(self, date):
        likes_dict = self.post_dao.getLikesPerDayDict()

        for post_date in likes_dict.keys():
            if post_date == date:
                numOfLikes = likes_dict[date]

        return numOfLikes

    def getLikesPerDay2(self,date):
        return jsonify(DateOfInterest = date, LikesPerDay = self.getLikesPerDay(date))


    def getDislikesPerDay(self, date):
        dislikes_dict = self.post_dao.getDislikesPerDayDict()

        for post in dislikes_dict.keys():
            if post == date:
                numOfDislikes = dislikes_dict[date]

        return numOfDislikes

    def getDislikesPerDay2(self,date):
        return jsonify(DateOfInterest = date, DislikesPerDay = self.getDislikesPerDay(date))


    def getAllStats(self, date):
        return jsonify(DateOfInterest = date, MostActiveUsers = self.getMostActiveUsers(date), RepliesPerDay = self.getRepliesPerDay(date),
                       LikesPerDay =  self.getLikesPerDay(date), DislikesPerDay = self.getDislikesPerDay(date), PostsPerDay = self.getPostsPerDay(date))

    def getStatByChoice(self, args, date):
        stat = args['stat']

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
        else:
            return jsonify(Error = "Invalid statistic operation"), 404
