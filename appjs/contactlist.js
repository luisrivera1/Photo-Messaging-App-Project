angular.module('AppChat').controller('ContactController', ['$http', '$log', '$scope', '$location', '$routeParams',
    function ($http, $log, $scope, $location, $routeParams) {

        var thisCtrl = this;
        this.contacts = [];


        this.loadContacts = function () {
            //TODO make this reqURL dynamic
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

            if(person != null)
            {
                var url = "http://localhost:5000/PhotoMsgApp/users/" + localStorage.getItem("id") + "/contacts"
                $http.post(url, ).then(function(response)){
                    console.log(response)
                    thisCtrl.push(response.data.)
                }

            }
            var reqURL = "http://localhost:5000/SocialMessagingApp/contactlist/adduser/" + thisCtrl.userId + "/" + thisCtrl.ctid;
            console.log("reqURL: " + reqURL);
//            data = {"owner_id": thisCtrl.currentUser.user_id, "username": username}
            // Now issue the http request to the rest API
            $http.get(reqURL).then(
                // Success function
                function (response) {
                    console.log("data: " + JSON.stringify(response.data));
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
                        //was added;
                    }
                });
            thisCtrl.ctid = "";

            $location.path('/home');

        };

        this.showChats = function () {
            $location.path('/home');
        };

        this.loadContacts();

    }]);