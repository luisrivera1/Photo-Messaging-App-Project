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

        this.deleteChat = function(){
        var chatname = prompt("Enter chat you wish to delete")

        if (chatname != null)
        {
            var id = localStorage.getItem("id");
            var url = "http://localhost:5000/PhotoMsgApp/chats"

            $http.get(url, { params : {"cname": chatname}}).then(function (response) {
                localStorage.setItem("chatid", response.data.Chat["cid"]);
                console.log(response.data.Chat);

                $http.delete(url, { params : {"uid" : id, "cid" : localStorage.getItem("chatid")}}).then(function(response){
                console.log(response.data)
                location.reload()

                })}).catch(function(err){
                    console.log(err)
                    alert("Chat could not be deleted!");
                });
          }



        }




        this.redirectToLogin = function () {
            localStorage.setItem("id", "");
            $window.location.href = '/#!/login';
            return
        }

        this.redirectToDashboard = function () {
            $window.location.href = '/#!/dashboard'
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
