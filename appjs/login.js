//var currentUser = "";

angular.module('AppChat').controller('LoginController', ['$http', '$log', '$scope', '$routeParams', '$window',
    function($http, $log, $scope, $routeParams, $window) {
        var thisCtrl = this;

        this.user = [];
        this.username = document.getElementById("username").value;
        this.password = document.getElementById("password").value;


        this.login = function(){
            //var chatid = $routeParams.cid;
            var parameter = JSON.stringify({"uusername": this.username, "upassword":this.password})
            var url = "http://localhost:5000/PhotoMsgApp/login";

            //console.log(parameter);
            //console.log($http.get(url, parameter));
                $http.post(url, parameter).then(function(data){
                    id_url = "http://localhost:5000/PhotoMsgApp/uid";

                    $http.get(id_url, { params : {"username": this.username.value}}).then(function(response)
                    {

                        localStorage.setItem("id",  response.data["ID"]);
                        console.log(localStorage.getItem("id"));
                        $window.location.href = '#!/home';
                    });
                }).catch(function(err){
                    alert("Invalid login");
                    $log.error(err.message);
                    $window.location.href = '#!/login';
                });
        };

        this.register = function(){
            $window.location.href = '#!/register';
        }
}]);
