var currentUser = "";
var currentUserId;

angular.module('AppChat').controller('LoginController', ['$http', '$log', '$scope', '$routeParams', '$window',
    function($http, $log, $scope, $routeParams, $window) {
        var thisCtrl = this;

        this.user = [];
        this.email = thisCtrl.email;
        this.password = thisCtrl.password;

        this.login = function(){
            //var chatid = $routeParams.cid;
            var parameter = JSON.stringify({email:this.email, password:this.password})
            var url = "http://localhost:63342/Photo-Messaging-App-ProjectLuisPhase3.3/index.html?_ijt=msi0963v0puohkauv6kdi3ada1#!/login"
                $http.post(url, parameter).then( function(data){
                    // Get the user from the server through the rest api

                    $log.log("User: ", JSON.stringify(data["data"]["User"]));
                    result = data["data"]["User"];
                    thisCtrl.user.push({
                        "uid":result["uid"],
                        "uusername":result["uusername"]
                    });
                    currentUser = result["uusername"];
                    currentUserId = result["uid"];
                    alert("Successful login for user : " + currentUser);
                    $window.location.href = '/#!/groups';

                }).catch(function(err){
                    alert("Invalid login");
                    $log.error(err.message);
                    $window.location.href = '/#!/login';
                });
        };

        this.register = function(){
            $window.location.href = '/Photo-Messaging-App-ProjectLuisPhase3.3/index.html?_ijt=ioe508iiudsdoq2o0jsmptfqpt#!/register';
        }
}]);
