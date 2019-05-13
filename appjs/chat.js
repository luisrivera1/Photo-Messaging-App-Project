angular.module('AppChat').controller('ChatController', ['$http', '$log', '$scope', '$rootScope', '$location', '$window', 'Upload', '$routeParams',
    function ($http, $log, $scope, $rootScope, $window, Upload, $location, $routeParams) {
        var thisCtrl = this;

        this.messageList = [];
        this.usersInChat = [];

        document.getElementById("chatname").innerHTML = localStorage.getItem("chatname")

        this.counter = 2;
        this.newText = "";

        this.loadUsers = function () {
            var chatname = localStorage.getItem("chatname");
            console.log(chatname);
            var id_url = "http://localhost:5000/PhotoMsgApp/chats";

            $http.get(id_url, { params : {"cname": chatname}}).then(function (response) {
                localStorage.setItem("chatid", response.data.Chat["cid"]);
                console.log(response)
                console.log(response.data)
            });


            //console.log(id);
            var id = localStorage.getItem("chatid");
            var url = "http://localhost:5000/PhotoMsgApp/chats/" + id + "/users";
            console.log(url)
            $http.get(url).then(function (response) {
                console.log("Response: " + JSON.stringify(response));
                console.log(response.data.UsersInChat);
                thisCtrl.usersInChat = response.data.UsersInChat;
            }).catch(function (response) {
                console.log(response)
                alert("No Users in Chat.");
            });
        };


        this.loadMessages = function () {
            // Get the messages from the server through the rest api
            // thisCtrl.messageList.push({"id": 1, "text": "Hola Mi Amigo", "author" : "Bob",
            //"like" : 4, "nolike" : 1});
            //thisCtrl.messageList.push({"id": 2, "text": "Hello World", "author": "Joe",
            //   "like" : 11, "nolike" : 12});

            var url = "http://localhost:5000/PhotoMsgApp/posts";


            $http.get(url).then(
                function (response) {
                    console.log("Response: " + JSON.stringify(response));
                    thisCtrl.messageList = response.data.Posts;
                }),
                function (response) {
                    console.log("Error response: " + JSON.stringify(response));
                    var status = response.status;

                    if (status == 0) {
                        alert("No internet connection");
                    } else if (status == 401) {
                        alert("Session has expired");
                    } else if (status == 403) {
                        alert("Authorization required");
                    } else if (status == 404) {
                        alert("Page not found");
                    } else {
                        alert("Internal system error has occurred");
                    }

                };
            $log.error("Message Loaded: ", JSON.stringify(thisCtrl.messageList));
        };

        this.postMsg = function () {
            var msg = thisCtrl.newText;
            // Need to figure out who I am
            var author = "Me";
            var nextId = thisCtrl.counter++;
            thisCtrl.messageList.unshift({
                "id": nextId,
                "p_message": msg,
                "p_user": author,
                "plikes": 0,
                "pdislikes": 0
            });
            thisCtrl.newText = "";
        };

        $scope.uploadPic = function (file) {
            Upload.upload({
                url: 'http://localhost:5000/PhotoMsgApp/posts',
                data: {file: file}
            })

            file.upload.then(function (response) {
                $timeout(function () {
                    file.result = response.data;
                });
            }, function (response) {
                if (response.status > 0)
                    $scope.errorMsg = response.status + ': ' + response.data;
            }, function (evt) {
                // Math.min is to fix IE which reports 200% sometimes
                file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
            });
        };

        this.redirectToHome = function () {
            window.location.href = '/#!/home';
        };

        this.loadUsers();
        this.loadMessages();

    }]);
