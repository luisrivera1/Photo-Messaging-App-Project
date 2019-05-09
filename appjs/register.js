angular.module('AppChat').controller('RegisterController', ['$http', '$log', '$scope', '$routeParams', '$window',
    function($http, $log, $scope, $routeParams, $window) {
        var thisCtrl = this;

        this.username = thisCtrl.username;
        this.firstname = thisCtrl.firstname;
        this.lastname = thisCtrl.lastname;
        this.password = thisCtrl.password;
        this.email = thisCtrl.email;

        this.register = function(){
            var userForm = new FormData();


            userForm.append("username", this.username);
            userForm.append("firstname", this.firstname);
            userForm.append("lastname", this.lastname);
            userForm.append("password", this.password);
            userForm.append("email", this.email);

            var url = "#!/register"
            //var reqURL = "https://quepasapp.herokuapp.com/QuePasApp/users/new";
            $http.post(url, userForm, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            }).then(  function(response){
                        // Get the user from the server through the rest api
                        result = response.data.userId;
                        $log.log(result);
                        alert("Valid registration for user: " + thisCtrl.username);
                        currentUser = thisCtrl.username;
                        currentUserId = result;
                        $window.location.href = '/#!/chat';

                }).catch(function(err){
                    alert("Invalid Register Field/s : " + err.message);
                    $log.error(err.message);
                    //$log.error(response.data);
                    $window.location.href = '/#!/register';
                });
        };
}]);
