angular.module('AppChat').controller('ChatController', ['$http', '$log', '$scope',
    function($http, $log, $scope) {
        var thisCtrl = this;

        this.messageList = [];
        this.counter  = 2;
        this.newText = "";

        this.loadMessages = function(){
            // Get the messages from the server through the rest api
           // thisCtrl.messageList.push({"id": 1, "text": "Hola Mi Amigo", "author" : "Bob",
            //"like" : 4, "nolike" : 1});
            //thisCtrl.messageList.push({"id": 2, "text": "Hello World", "author": "Joe",
             //   "like" : 11, "nolike" : 12});

            var url = "http://localhost:5000/PhotoMsgApp/posts/chat"

            chatname = localStorage.getItem("chatname");
            //console.log(params)

            $http.get(url, { params : {"chatname" : chatname } }).then(
                function(response){
                    console.log("Response: "+JSON.stringify(response));
                    thisCtrl.messageList = response.data.Posts
                },
                function(response){
                    console.log("Error response: "+JSON.stringify(response));
                    var status = response.status;

                    if(status==0){
                        alert("No internet connection");
                    }
                    else if (status == 401) {
                        alert("Session has expired");
                    }
                    else if (status == 403) {
                        alert("Authorization required");
                    }
                    else if (status == 404){
                        alert("Page not found");
                    }
                    else {
                        alert("Internal system error has occurred");
                    }

                }


            )

            $log.error("Message Loaded: ", JSON.stringify(thisCtrl.messageList));
        };

        this.postMsg = function(){
            var msg = thisCtrl.newText;
            // Need to figure out who I am
            var author = "Me";
            var nextId = thisCtrl.counter++;
            thisCtrl.messageList.unshift({"id": nextId, "p_message" : msg, "p_user" : author, "plikes" : 0, "pdislikes" : 0});
            thisCtrl.newText = "";
        };

        this.loadMessages();
}]);