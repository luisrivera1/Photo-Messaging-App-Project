from handler import postHandler
from flask import jsonify
from operator import itemgetter
from dao.users import usersDAO
from dao.stats import statsDAO



class statHandler:
    def __init__(self):
        self.post_dao = postHandler.postsDAO()

    def build_post_per_user_per_day_stat_dict(self, row, dates):
        result = {}

        result['pid'] = row[0]
        result['p_user'] = row[1]
        result['p_photo'] = row[2]
        result['p_message'] = row[3]
        return result

    # def getMostActiveUsers(self, date):
    #     user_dict = self.post_dao.getUsersDictByDay(date)
    #     print(user_dict)
    #
    #     sorted_dict = sorted(user_dict.items(), key = itemgetter(1), reverse = True)
    #
    #     print(sorted_dict)
    #
    #     mostActiveUsers = [sorted_dict[0][0], sorted_dict[1][0], sorted_dict[2][0]]
    #
    #     return mostActiveUsers
    #
    #
    # def getMostActiveUsers2(self,date):
    #     return jsonify(DateOfInterest = date, MostActiveUsers = self.getMostActiveUsers(date))
    #
    # def getRepliesPerDay(self, date):
    #     replies_dict = self.post_dao.getRepliesPerDayDict()
    #
    #     for post_date in replies_dict.keys():
    #         if post_date == date:
    #             numOfReplies = replies_dict[date]
    #             return numOfReplies
    #     return 0
    #
    # def getRepliesPerDay2(self,date):
    #     return jsonify(DateOfInterest = date, RepliesPerDay=self.getRepliesPerDay(date))
    #
    # def getPostsPerDay(self, date):
    #     post_dict = self.post_dao.getPostPerDayDict()
    #     for post_date in post_dict.keys():
    #         if post_date == date:
    #             numOfPosts = post_dict[date]
    #             return numOfPosts
    #
    #     return 0
    #
    # def getPostsPerDay2(self,date):
    #     return jsonify(DateOfInterest = date, PostPerDay = self.getPostsPerDay(date))
    #
    #
    # def getLikesPerDay(self, date):
    #     likes_dict = self.post_dao.getLikesPerDayDict()
    #
    #     for post_date in likes_dict.keys():
    #         if post_date == date:
    #             numOfLikes = likes_dict[date]
    #             return numOfLikes
    #
    #     return None
    #
    # def getLikesPerDay2(self,date):
    #     return jsonify(DateOfInterest = date, LikesPerDay = self.getLikesPerDay(date))
    #
    #
    # def getDislikesPerDay(self, date):
    #     dislikes_dict = self.post_dao.getDislikesPerDayDict()
    #
    #     for post in dislikes_dict.keys():
    #         if post == date:
    #             numOfDislikes = dislikes_dict[date]
    #             return numOfDislikes
    #
    #     return None
    #
    # def getDislikesPerDay2(self,date):
    #     return jsonify(DateOfInterest = date, DislikesPerDay = self.getDislikesPerDay(date))
    #
    # def getAllStats(self, date):
    #     return jsonify(DateOfInterest=date, MostActiveUsers=self.getMostActiveUsers(date), RepliesPerDay=self.getRepliesPerDay(date),
    #                    LikesPerDay=self.getLikesPerDay(date), DislikesPerDay=self.getDislikesPerDay(date), PostsPerDay=self.getPostsPerDay(date))
    #
    # def getPostsPerDayByUser(self, user, date):
    #     user_post_dict = self.post_dao.getUserPostsByDateDict(user, date)
    #
    #     for post in user_post_dict.keys():
    #         if post == user:
    #             numOfPostsByUser = user_post_dict[user]
    #             return numOfPostsByUser
    #
    #     return 0
    #
    # def getPostsPerDayByUser2(self, user):
    #     return jsonify(DateOfInterest = date, UserOfInterest = user, PostsPerDay = self.getPostsPerDayByUser(user, date))
    #
    # def getRepliesPerPhoto(self, photo):
    #     photo_reply_dict = self.post_dao.getPhotoRepliesDict(photo)
    #
    #     for picture in photo_reply_dict.keys():
    #         if picture == photo:
    #             numOfPhotoReplies = photo_reply_dict[photo]
    #             return numOfPhotoReplies
    #
    #     return 0
    #
    # def getRepliesPerPhoto2(self, photo):
    #     return jsonify(PhotoOfInterest = photo, NumberOfReplies = self.getRepliesPerPhoto(photo))
    #
    # def getLikesPerPhoto(self, photo):
    #     photo_likes_dict = self.post_dao.getPhotoLikesDict(photo)
    #
    #     for picture in photo_likes_dict.keys():
    #         if picture == photo:
    #             numOfPhotoLikes = photo_likes_dict[photo]
    #             return numOfPhotoLikes
    #
    #     return None
    #
    # def getLikesPerPhoto2(self, photo):
    #     return jsonify(PhotoOfInterest = photo, NumberOfLikes = self.getLikesPerPhoto(photo))
    #
    # def getDislikesPerPhoto(self, photo):
    #     photo_dislikes_dict = self.post_dao.getPhotoDislikesDict(photo)
    #
    #     for picture in photo_dislikes_dict.keys():
    #         if picture == photo:
    #             numOfPhotoDislikes = photo_dislikes_dict[photo]
    #             return numOfPhotoDislikes
    #
    #     return None
    #
    # def getDislikesPerPhoto2(self, photo):
    #     return jsonify(PhotoOfInterest = photo, NumberOfDislikes = self.getDislikesPerPhoto(photo))

    def getTrendingHashtagsTotal(self):
        dao = statsDAO()
        dates = dao.getAvailableTrendingDates()
        if not dates:
            return jsonify(Error="No hashtags found"), 400
        return jsonify(TrendingHashtags=dao.getTrendringHashtagsTotal(dates)), 200

    def getTrendingHashtagsTotal(self):
        dao = statsDAO()
        dates = dao.getAvailableTrendingDates()
        if not dates:
            return jsonify(Error="No hashtags found"), 400
        return jsonify(TrendingHashtags=dao.getTrendringHashtagsTotal(dates)), 200

    def getMostActiveUsers(self):
        dao = statsDAO()
        dates = dao.getPostDatesAvailable()
        if not dates:
            return jsonify(Error="No Posts found"), 400
        return jsonify(MostActiveUsersPerDates=dao.getMostActiveUsers(dates)), 200

    def getStatByChoice(self, form):
        stat = form['stat']
        dao = statsDAO()
        if len(form) == 2:
            uid = form['uid']
            if stat == "postsperdaybyuser":
                dao2 = usersDAO()
                if not dao2.getUserById(uid):
                    return jsonify(Error="User " + str(uid) + " not found"), 404
                dates = dao.getDatesOfPostsPerDayByUser(uid)
                if not dates:
                    return jsonify(Error="No Posts found for user: " + str(uid)), 400
                result_list = dao.getPostsPerDayByUser(uid, dates)
                # result_list = []
                # for row in posts_count_list:
                #     result = self.build_post_per_user_per_day_stat_dict(row)
                #     result_list.append(result)
                return jsonify(PostsPerDayOfUser=result_list), 200
            return jsonify(Error="Invalid statistic per user operation"), 404
        if len(form) == 1:
            if stat == "mostactiveusers":
                dates = dao.getPostDatesAvailable()
                if not dates:
                    return jsonify(Error="No Posts found"), 400
                return jsonify(MostActiveUsersPerDates=dao.getMostActiveUsers(dates)), 200
            elif stat == "repliesperdates":
                dates = dao.getAvailableRepliesDates()
                if not dates:
                    return jsonify(Error="No replies found"), 400
                return jsonify(RepliesPerDates=dao.getRepliesPerDates(dates)), 200
            elif stat == "postsperdates":
                dates = dao.getPostDatesAvailable()
                if not dates:
                    return jsonify(Error="No Posts found"), 400
                return jsonify(PostsPerDates=dao.getPostsPerDates(dates)), 200
            elif stat == "likesperdates":
                dates = dao.getReactionsDatesAvailable()
                if not dates:
                    return jsonify(Error="No reactions found"), 400
                return jsonify(LikesPerDates=dao.getLikesPerDate(dates)), 200
            elif stat == "dislikesperdates":
                dates = dao.getReactionsDatesAvailable()
                if not dates:
                    return jsonify(Error="No reactions found"), 400
                return jsonify(Dislikes=dao.getDisikesPerDate(dates)), 200
            elif stat == "trending":
                dates = dao.getAvailableTrendingDates()
                if not dates:
                    return jsonify(Error="No hashtags found"), 400
                return jsonify(TrendingHashtags=dao.getTrendringHashtags(dates)), 200
            return jsonify(Error="Invalid statistic operation"), 404
        return jsonify(Error="Malformed stats request"), 400

    # def getPhotoStatsByChoice(self, args, photo):
    #     stat = args['stat']
    #
    #     if stat == "replies":
    #         return self.getRepliesPerPhoto2(photo)
    #     elif stat == "likes":
    #         return self.getLikesPerPhoto2(photo)
    #     elif stat == "dislikes":
    #         return self.getDislikesPerPhoto2(photo)
    #     else:
    #         return jsonify(Error="Invalid statistic operation"), 404
    #
    # def getAllPhotoStats(self, photo):
    #     return jsonify(PhotoOfInterest = photo, NumberOfReplies = self.getRepliesPerPhoto(photo), NumberOfLikes = self.getLikesPerPhoto(photo),
    #                    NumberOfDislikes =  self.getDislikesPerPhoto(photo))
