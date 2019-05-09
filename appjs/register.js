angular.module('AppChat').controller('RegisterController', ['$http', '$log', '$scope', '$routeParams', '$window',
    function($http, $log, $scope, $routeParams, $window) {
        var thisCtrl = this;

        this.username = thisCtrl.username;
        this.firstname = thisCtrl.firstname;
        this.lastname = thisCtrl.lastname;
        this.password = thisCtrl.password;
        this.email = thisCtrl.email;

        this.register = function(){
           // var userForm = new FormData();


//            userForm.append("username", this.username);
//            userForm.append("firstname", this.firstname);
//            userForm.append("lastname", this.lastname);
//            userForm.append("password", this.password);
//            userForm.append("email", this.email);
            this.firstname = document.getElementById("firstname").value;
            this.lastname = document.getElementById("lastname").value;
            this.email = document.getElementById("email").value;
            this.username = document.getElementById("username").value;
            this.password = document.getElementById("password").value;



            var url = "http://localhost:5000/PhotoMsgApp/register";
            var param = JSON.stringify({"ufirstname":this.firstname, "ulastname": this.lastname, "uemail": this.email,
                                        "uusername":this.username, "upassword":this.password})
            //var reqURL = "https://quepasapp.herokuapp.com/QuePasApp/users/new";
            $http.post(url, param).then( function(response){
                        alert("Valid registration for user: " + this.username);
                        $window.location.href = '/#!/login';

                }).catch(function(err){
                    alert("Invalid Register Field/s : " + err.message);
                    $log.error(err.message);
                    //$log.error(response.data);
                    $window.location.href = '/#!/register';
                });
        };
}]);
