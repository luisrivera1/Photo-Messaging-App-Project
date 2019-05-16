angular.module('AppChat').controller('ContactController', ['$http', '$log', '$scope', '$location', '$routeParams', '$window',
    function ($http, $log, $scope, $location, $routeParams, $window) {

        var thisCtrl = this;
        this.contacts = [];

       console.log(localStorage.getItem("id"));
        this.loadContacts = function () {
            // alert(this.uid);
            var url = "http://localhost:5000/PhotoMsgApp/users/" + localStorage.getItem("id") + "/contacts";
            // Now issue the http request to the rest API
            $http.get(url).then(
                // Success function
                function (response) {
                    /*
                    * Stores the data received from python call. The jsonyfied data
                    */
                    thisCtrl.contacts = response.data.ContactList;
                    console.log(thisCtrl.contacts);
                },
                function (response) {
                    // This is the error function
                    // If we get here, some error occurred.
                    // Verify which was the cause and show an alert.
                    var status = response.status;
                    if (status === 0) {
                        alert("No hay conexion a Internet");
                    } else if (status === 401) {
                        alert("Su sesion expiro. Conectese de nuevo.");
                    } else if (status === 403) {
                        alert("No esta autorizado a usar el sistema.");
                    } else if (status === 404) {

                    } else {

                    }
                });

            $log.debug("Contact list Loaded: ", JSON.stringify(thisCtrl.contacts));
        };

        this.addContact = function () {
            var username = prompt("Enter the username of the person you wish to add");

            if(username != null || username != "")
            {
                var url = "http://localhost:5000/PhotoMsgApp/users/" + localStorage.getItem("id") + "/contacts"
                var param = JSON.stringify({"cusername" :  username});
                $http.post(url, param).then(function(response){
                    console.log(response)
                    this.contacts.push(response.data.Contact)
                    alert("Contact added");
                 }).catch(function (response) {
                console.log(response)
                alert("Contact NOT added");
            });
            }
             else{
                alert("No user with that username exists.");
              };
            location.reload()

        };

        this.showChats = function () {
            $location.path('/home');
        };

        this.loadContacts();

      }]);

