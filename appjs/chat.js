angular.module('AppChat').controller('ChatController', ['$http', '$log', '$scope', '$rootScope', '$location', '$window', 'Upload', '$routeParams',
    function ($http, $log, $scope, $rootScope, $window, Upload, $location, $routeParams) {
        var thisCtrl = this;

        this.messageList = [];
        this.usersInChat = [];

        document.getElementById("chatname").innerHTML = localStorage.getItem("chatname")

        this.chatname = localStorage.getItem("chatname");
        this.counter = 2;
        this.newText = "";

        this.loadUsers = function () {
            console.log(this.chatname);
            var id_url = "http://localhost:5000/PhotoMsgApp/chats";

            $http.get(id_url, { params : {"cname": this.chatname}}).then(function (response) {
                localStorage.setItem("chatid", response.data.Chat["cid"]);
                console.log(response.data.Chat)

                     //console.log(id);
                var id = localStorage.getItem("chatid");
                var url = "http://localhost:5000/PhotoMsgApp/chats/" + id + "/users";
                console.log(url)
                $http.get(url).then(function (response) {
                    console.log("Response: " + JSON.stringify(response));
                    console.log(response.data.UsersInChat);
                    thisCtrl.usersInChat = response.data.UsersInChat;
            })
            });



        };


        this.loadMessages = function () {
            // Get the messages from the server through the rest api
            // thisCtrl.messageList.push({"id": 1, "text": "Hola Mi Amigo", "author" : "Bob",
            //"like" : 4, "nolike" : 1});
            //thisCtrl.messageList.push({"id": 2, "text": "Hello World", "author": "Joe",
            //   "like" : 11, "nolike" : 12});

            var url = "http://localhost:5000/PhotoMsgApp/posts/chat/original";
            //var chatname = localStorage.getItem("chatname");

            console.log(url)
            console.log(this.chatname)

            $http.get(url, { params : {"chatname": this.chatname}}).then(
                function (response) {
                    console.log("Response: " + JSON.stringify(response));
                    thisCtrl.messageList = response.data.Posts;
                });

        };
        //
        // this.loadReplies = function() {
        //     var url = 'http://localhost:5000/posts/' +
        // }

//        this.uploadPic = function (file) {
//            console.log(file);
//            var id = localStorage.getItem("id");
//            var photo =  "http://localhost:5000/static/";
//            var url = "http://localhost:5000/PhotoMsgApp/posts";
//            var message = $scope.message;
//            console.log(photo);
//            console.log(message);
//
//
//            var data = JSON.stringify({"puser": id, "pphoto": file, "pmessage": $scope.message, "pdate" : new Date(), "cname" : localStorage.getItem("chatname")});
            //$http.post(url, data).then(function(response){
            //    console.log(response.data);
                //this.messageList.push(response.data.Post);
            //});

//
//            file.upload.then(function (response) {
//                $timeout(function () {
//                    file.result = response.data;
//                });
//            }, function (response) {
//                if (response.status > 0)
//                    $scope.errorMsg = response.status + ': ' + response.data;
//            }, function (evt) {
//                // Math.min is to fix IE which reports 200% sometimes
//                file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
//            });
 //       };

//         this.deleteUserFromChat = function () {
//             //console.log(this.chatname);
//             var id = localStorage.getItem("chatid");
//             var id_url = "http://localhost:5000/PhotoMsgApp/chats/" + id + "/user/" + uid + 00000000;
// /PhotoMsgApp/chats/<int:cid>/user/<int:admin_id>/delete/<int:uid>'
//             $http.get(id_url, { params : {"cname": this.chatname}}).then(function (response) {
//                 localStorage.setItem("chatid", response.data.Chat["cid"]);
//                 console.log(response.data.Chat)
//
//                      //console.log(id);
//
//                 var url = "http://localhost:5000/PhotoMsgApp/chats/" + id + "/users";
//                 console.log(url)
//                 $http.get(url).then(function (response) {
//                     console.log("Response: " + JSON.stringify(response));
//                     console.log(response.data.UsersInChat);
//                     thisCtrl.usersInChat = response.data.UsersInChat;
//             })
//             });
//
//
//
//         };

        this.redirectToHome = function () {
            window.location.href = '/#!/home';
        };

        this.redirectToReplies = function() {
            window.location.href = '/#!/reply'
        };

        this.addUserToChat = function(){
            var username = prompt("Enter username of user to insert.")

            if(username != null)
            {
                var cid = localStorage.getItem("chatid");

                var url = "http://localhost:5000/PhotoMsgApp/uid"

                $http.get(url, { params : { "username" : username } }).then(function(response){
                     console.log(response.data)
                     var contact_id = response.data["ID"];

                     url = "http://localhost:5000/chats/contacts/";
                     console.log(url)

                     data = JSON.stringify({"cid": cid, "contact_id": contact_id})
                     $http.post(url, data, { headers: {
                      'Access-Control-Allow-Origin': '*',
                      'Access-Control-Allow-Methods': ['POST', 'OPTIONS', 'PUT'],
                      'Access-Control-Allow-Headers': ["Access-Control-Allow-Origin", "Access-Control-Allow-Methods", "Content-Type"],
                      'Content-Type': 'application/json',  // <-- here
                    }}).then(function(response2){
                        console.log(response2.data)
                        this.usersInChat.push(response2.data.AddedChatMember)
                        location.reload()
                     }).catch(function(){
                         alert("User could not be added to chat.")
                     });
                });
            };

        };

       this.addLike = function (post) {
           var today = new Date();
           var dd = today.getDate();
           var mm = today.getMonth() + 1; //January is 0!
           var yyyy = today.getFullYear();
           today = dd + '-' + mm + '-' + yyyy; // pdate

           var type = "like";
           var usr = localStorage.getItem("id");
           var post = document.activeElement.getAttribute("value")

           var url = "http://localhost:5000/posts/" + post + "/likes/" + usr;

           $http.put(url, {  headers: {
      'Access-Control-Allow-Origin': 'http://localhost:5000/PhotoMsgApp/login',
      'Content-Type': 'application/json',  // <-- here
      'Authorization': 'Basic clopez26:password'
    }}).then(function(response){
                console.log(response)
                location.reload()
           })
       };

       this.addDislike = function(post) {
           var today = new Date();
           var dd = today.getDate();
           var mm = today.getMonth() + 1; //January is 0!
           var yyyy = today.getFullYear();
           today = dd + '-' + mm + '-' + yyyy; // pdate

           var usr = localStorage.getItem("id");
           var post = document.activeElement.getAttribute("value")
           var type = "like";

           var url = "http://localhost:5000/posts/" + post + "/dislikes/" + usr;

           $http.put(url, { headers: {
      'Access-Control-Allow-Origin': 'http://localhost:5000/PhotoMsgApp/login',
      'Content-Type': 'application/json',  // <-- here
      'Authorization': 'Basic clopez26:password'
    }}).then(function(response){
               console.log(response)
               location.reload()
           })

       };

//            // Build the data object
//            var data = {};
//            data.post_id = post['postId'];
//            data.react_type = 1;
//            //TODO: remove user_id
//            data.user_id = this.user;
//
//            // Now create the url with the route to talk with the rest API
//            var reqURL = "http://localhost:5000/Pictochat/post/react";
//            console.log("reqURL: " + reqURL);
//
//            // configuration headers for HTTP request
//            var config = {
//                withCredentials: true,
//                headers: {
//                    'Content-Type': 'application/json;charset=utf-8;'
//                }
//            };
//            $http.post(reqURL, data, config).then(
//                // Success function
//                function ((response) {
//                    console.log("data: " + JSON.stringify(response.data));
//                    // tira un mensaje en un alert
//                    console.log("Post " + response.data.React.post_id + " Liked");
//                    post.dislikes = response.data.React.totalDislikes;
//                    post.likes = response.data.React.totalLikes;
//                   // M.toast({html: 'Post Liked!'})
//                )};
//            );
//        };

        this.loadUsers();
        this.loadMessages();

    }]);
