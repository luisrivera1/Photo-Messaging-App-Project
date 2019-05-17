angular.module('AppChat').controller('HomeController', ['$http', '$log', '$scope', '$routeParams', '$window',
    function ($http, $log, $scope, $routeParams, $window) {

        var thisCtrl = this;
        this.groupList = [];
        this.newGroup = "";

        this.loadGroups = function () {
            id = localStorage.getItem("id");
            console.log(id);
            var url = "http://localhost:5000/PhotoMsgApp/users/" + id + "/chats";
            console.log(url)
            $http.get(url).then(function (response) {
                console.log("Response: " + JSON.stringify(response));
                console.log(response.data.Chats)
                thisCtrl.groupList = response.data.Chats
            }).catch(function (response) {
                console.log(response)
                alert("User has no chats.");
            });
        };


        this.createChat = function(){
           var chatname = prompt("Enter chat name.")

           if (chatname != null)
           {
                var id = localStorage.getItem("id");
                var url = "http://localhost:5000/PhotoMsgApp/chats"

                data = JSON.stringify({"cname" : chatname, "cadmin" : id})
                $http.post(url, data).then(function (response){
                    console.log(response.data)
                    this.groupList.push(response.data.Chat)
                });
            }

            location.reload()
        }

        this.redirectToLogin = function () {
            localStorage.setItem("id", "");
            $window.location.href = '/#!/login';
            return
        }

        this.redirectToDashboard = function () {
            $window.location.href = '/#/dashboard'
        }

        this.redirectToContactList = function () {
            $window.location.href = '/#!/contactlist';
            return
        }

        this.redirectToChat = function () {
            console.log(document.activeElement.getAttribute("value"));
            localStorage.setItem("chatname", document.activeElement.getAttribute("value"));
            $window.location.href = '/#!/chat'
        }

        this.loadGroups();
    }]);
