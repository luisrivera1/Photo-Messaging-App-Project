angular.module('AppChat').controller('GroupsController', ['$http', '$log', '$scope', '$routeParams', '$window',
    function($http, $log, $scope, $routeParams, $window) {

        var thisCtrl = this;
        this.groupList = [];
        this.newGroup = "";

        this.loadGroups = function(){

            //var chatid = $routeParams.cid;
            var url = "http://localhost:5000/PhotoMsgApp/chats"

                $http.get(url).then(function(response){
                    console.log("Response: "+JSON.stringify(response));
                    console.log(currentUser)
                    thisCtrl.groupList = response.data.Chats
                    })};

        this.redirectToLogin = function(){
            $window.location.href = '/#!/login';
            return
        }

        this.redirectToJoinGroups = function(){
            $window.location.href = '/#!/joinGroups';
            return
        }

        this.loadGroups();
}]);
