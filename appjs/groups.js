angular.module('AppChat').controller('GroupsController', ['$http', '$log', '$scope', '$routeParams', '$window',
    function($http, $log, $scope, $routeParams, $window) {

        var thisCtrl = this;
        this.groupList = [];
        this.newGroup = "";

        this.loadGroups = function(){
            console.log(currentUser);

            var url = "http://localhost:5000/PhotoMsgApp/users/" + currentUser + "/chats";
            console.log(url)
                $http.get(url).then(function(response){
                    console.log("Response: "+JSON.stringify(response));
                    console.log(response.data.Chats)
                    thisCtrl.groupList = response.data.Chats
                    }).catch(function(response){
                       console.log(response)
                       alert("User has no chats.");
                    });
                 };

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
