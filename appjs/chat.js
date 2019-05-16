angular.module('AppChat').controller('ChatController', ['$http', '$log', '$scope', '$rootScope', '$location', '$window', '$timeout', '$routeParams', 'Upload', '$route',
    function ($http, $log, $scope, $rootScope, $location, $window, $timeout, $routeParams, Upload, $route) {
        var thisCtrl = this;

        this.messageList = [];
        this.usersInChat = [];

        document.getElementById("chatname").innerHTML = localStorage.getItem("chatname");

        this.chatname = localStorage.getItem("chatname");
        this.counter = 2;
        this.newText = "";
        this.filename = "";
        this.contactId;

        this.loadUsers = function () {
            var chatname = localStorage.getItem("chatname");
            console.log(chatname);
            var id_url = "http://localhost:5000/PhotoMsgApp/chats";

            $http.get(id_url, {params: {"cname": chatname}}).then(function (response) {
                localStorage.setItem("chatid", response.data.Chat["cid"]);
                console.log(response);
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
                console.log(response);
                alert("No Users in Chat.");
            });
        };

        // this.addUsers = function () {
        //     var chatname = localStorage.getItem("chatname");
        //     console.log(chatname);
        //     var id_url = "http://localhost:5000/PhotoMsgApp/chats";
        //
        //     $http.get(id_url, {params: {"cname": chatname}}).then(function (response) {
        //         localStorage.setItem("chatid", response.data.Chat["cid"]);
        //         console.log(response);
        //         console.log(response.data)
        //     });
        //
        //     var id = localStorage.getItem("chatid");
        //     var username = prompt("Enter the username of the person you wish to add");
        //
        //     if (username != null) {
        //         var url = "http://localhost:5000/PhotoMsgApp/chats/" + id + "/contacts/" + localStorage.getItem("chatname");
        //         var param = JSON.stringify({"cusername": username});
        //         $http.post(url, param).then(function (response) {
        //             console.log(response);
        //             this.usersInChat.push(response.data.AddedChatMember)
        //
        //         })
        //     } else {
        //         alert("No user with that username exists.");
        //     }
        //
        // };

        this.loadMessages = function () {
            // Get the messages from the server through the rest api
            // thisCtrl.messageList.push({"id": 1, "text": "Hola Mi Amigo", "author" : "Bob",
            //"like" : 4, "nolike" : 1});
            //thisCtrl.messageList.push({"id": 2, "text": "Hello World", "author": "Joe",
            //   "like" : 11, "nolike" : 12});

            var url = "http://localhost:5000/PhotoMsgApp/posts/chat/original";
            //var chatname = localStorage.getItem("chatname");

            console.log(url);
            console.log(this.chatname);

            $http.get(url, {params: {"chatname": this.chatname}}).then(
                function (response) {
                    console.log("Response: " + JSON.stringify(response));
                    thisCtrl.messageList = response.data.Posts;
                });

        };
        //
        // this.loadReplies = function() {
        //     var url = 'http://localhost:5000/posts/' +
        // }

        // this.postMsg = function () {
        //     var msg = thisCtrl.newText;
        //     // Need to figure out who I am
        //     var author = "Me";
        //     var nextId = thisCtrl.counter++;
        //     thisCtrl.messageList.unshift({
        //         "id": nextId,
        //         "p_message": msg,
        //         "p_user": author,
        //         "plikes": 0,
        //         "pdislikes": 0
        //     });
        //     thisCtrl.newText = "";
        // };

        // $scope.uploadPic = function (file) {
        //     Upload.upload({
        //         url: 'http://localhost:5000/PhotoMsgApp/posts',
        //         data: {file: file}
        //     })
        //
        //     file.upload.then(function (response) {
        //         $timeout(function () {
        //             file.result = response.data;
        //         });
        //     }, function (response) {
        //         if (response.status > 0)
        //             $scope.errorMsg = response.status + ': ' + response.data;
        //     }, function (evt) {
        //         // Math.min is to fix IE which reports 200% sometimes
        //         file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
        //     });
        // };

        $scope.uploadPic = function (file) {

            file.upload = Upload.upload({
                url: 'http://localhost:5000/PhotoMsgApp/post/new',
                data: {
                    "puser": localStorage.getItem("id"),
                    file: file,
                    "pmessage": $scope.message,
                    "pdate": new Date(),
                    "chatName": localStorage.getItem("chatname")
                }
            });

            file.upload.then(function (response) {

                $timeout(function () {
                    file.result = response.data;
                    //TODO: implement push and remove relod.
                    // thisCtrl.postList.push(response.data.Post);
                    // $scope.file = "";
                    // $scope.message = "";
                    $route.reload()
                });
            }, function (response) {
                if (response.status > 0)
                    $scope.errorMsg = response.status + ': ' + response.data;
            }, function (evt) {
                // Math.min is to fix IE which reports 200% sometimes
                file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
            });


        };

        //         this.likeAdd = function (post) {
        //     // Build the data object
        //     var data = {};
        //     data.post_id = post['postId'];
        //     data.react_type = 1;
        //     //TODO: remove user_id
        //     data.user_id = this.user;
        //
        //     // Now create the url with the route to talk with the rest API
        //     var reqURL = "http://localhost:5000/Pictochat/post/react";
        //     console.log("reqURL: " + reqURL);
        //
        //     // configuration headers for HTTP request
        //     var config = {
        //         withCredentials: true,
        //         headers: {
        //             'Content-Type': 'application/json;charset=utf-8;'
        //         }
        //     };
        //     $http.post(reqURL, data, config).then(
        //         // Success function
        //         function (response) {
        //             console.log("data: " + JSON.stringify(response.data));
        //             // tira un mensaje en un alert
        //             console.log("Post " + response.data.React.post_id + " Liked");
        //             post.dislikes = response.data.React.totalDislikes;
        //             post.likes = response.data.React.totalLikes;
        //             M.toast({html: 'Post Liked!'})
        //
        //         }, //Error function
        //         function (response) {
        //
        //             var status = response.status;
        //
        //             if (status === 0) {
        //                 alert("No hay conexion a Internet");
        //             } else if (status === 401) {
        //                 alert("Su sesion expiro. Conectese de nuevo.");
        //             } else if (status === 403) {
        //                 alert("No esta autorizado a usar el sistema.");
        //             } else if (status === 404) {
        //                 alert("No se encontro la informacion solicitada.");
        //             } else {
        //                 alert("Error interno del sistema.");
        //             }
        //         }
        //     );
        // };

        this.redirectToHome = function () {
            window.location.href = '/#!/home';
        };

        this.redirectToReplies = function () {
            window.location.href = '/#!/reply'
        };


        this.postMsg = function () {
            var msg = thisCtrl.newText;
            var url = "http://127.0.0.1:5000/PhotoMsgApp/posts";


            var today = new Date();
            var dd = today.getDate();
            var mm = today.getMonth() + 1; //January is 0!
            var yyyy = today.getFullYear();
            today = dd + '-' + mm + '-' + yyyy;

            media = '';


            if (thisCtrl.filename != null && thisCtrl.filename != '' && thisCtrl.filename != ' ') {

                media = "http://localhost:5000/static/" + thisCtrl.filename;

                data = {"puser": localStorage.getItem("id"), "pphoto": media, "pmessage": msg, "pdate": today};

                $http.post(url, data).then(function (response) {
                        console.log("data: " + JSON.stringify(response.data));
                        this.messageList.push(response.data.Posts);

                    }
                );
            }
            ;

        };

        $scope.thumbnail = [];
        // Read the image using the filereader
        $scope.fileReaderSupported = window.FileReader != null;
        $scope.photoChanged = function (files) {
            if (files != null) {
                var file = files[0];
                if ($scope.fileReaderSupported && file.type.indexOf('image') > -1) {
                    $timeout(function () {
                        var fileReader = new FileReader();
                        fileReader.readAsDataURL(file); // convert the image to data url.
                        fileReader.onload = function (e) {
                            $timeout(function () {
                                console.log(file.name); // Retrieve the image.
                                thisCtrl.filename = file.name;
                                $scope.filename = file.name;
                                $scope.p_photo = e.target.result;
                            });
                        }
                    });
                }
            }
        };

        this.loadUsers();
        this.loadMessages();

        //insert like on post
        this.likeAdd = function (post) {
            // Build the data object
            var data = {};
            data.post = post['pid'];
            data.type = 'like';
            //TODO: remove user_id
            data.usr = localStorage.getItem("id");

            // Now create the url with the route to talk with the rest API
            var reqURL = "http://localhost:5000/PhotoMsgApp/posts/" + data.post + "/likes/" + data.usr;
            console.log("reqURL: " + reqURL);

            // configuration headers for HTTP request
            var config = {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json;charset=utf-8;'
                }
            };
            $http.post(reqURL, data, config).then(
                // Success function
                function (response) {
                    console.log("data: " + JSON.stringify(response.data));
                    // tira un mensaje en un alert
                    // console.log("Post " + response.data.React.post_id + " Liked");
                    // post.plikes = response.data.React.UpdatedLikesOfPost.plikes;
                    $route.reload();

                }, //Error function
                function (response) {

                    var status = response.status;

                    if (status === 0) {
                        alert("No hay conexion a Internet");
                    } else if (status === 401) {
                        alert("Su sesion expiro. Conectese de nuevo.");
                    } else if (status === 403) {
                        alert("No esta autorizado a usar el sistema.");
                    } else if (status === 404) {
                        alert("No se encontro la informacion solicitada.");
                    } else {
                        alert("Error interno del sistema.");
                    }
                }
            );
        };
        //insert like on post
        this.dislikeAdd = function (post) {
            // Build the data object
            var data = {};
            data.post = post['pid'];
            data.type = 'like';
            //TODO: remove user_id
            data.usr = localStorage.getItem("id");

            // Now create the url with the route to talk with the rest API
            var reqURL = "http://localhost:5000/PhotoMsgApp/posts/" + data.post + "/dislikes/" + data.usr;
            console.log("reqURL: " + reqURL);

            // configuration headers for HTTP request
            var config = {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json;charset=utf-8;'
                }
            };
            $http.post(reqURL, data, config).then(
                // Success function
                function (response) {
                    console.log("data: " + JSON.stringify(response.data));
                    $route.reload();

                }, //Error function
                function (response) {

                    var status = response.status;

                    if (status === 0) {
                        alert("No hay conexion a Internet");
                    } else if (status === 401) {
                        alert("Su sesion expiro. Conectese de nuevo.");
                    } else if (status === 403) {
                        alert("No esta autorizado a usar el sistema.");
                    } else if (status === 404) {
                        alert("No se encontro la informacion solicitada.");
                    } else {
                        alert("Error interno del sistema.");
                    }
                }
            );
        };

        this.addUserToChat = function () {
            var username = prompt("Enter username of user to insert.");

            if (username != null) {
                var cid = localStorage.getItem("chatid");

                var url = "http://localhost:5000/PhotoMsgApp/uid";
                 var config = {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json;charset=utf-8;'
                }
            };

                $http.get(url, {params: {"username": username}}, config).then(
                    function (response) {
                        console.log(response.data);
                        thisCtrl.contactId = response.data["ID"];
                        thisCtrl.addUserToChat2();
                    });
            };
              this.addUserToChat2 = function () {

                var url = "http://localhost:5000/chats/contacts/";
                console.log(url);
                var data = {};

                 var config = {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json;charset=utf-8;'
                }
            };
                data = {"cid": cid, "contact_id": thisCtrl.contactId};
                $http.post(url, data, config).then(
                    function (response) {
                    console.log(response.data);
                    this.usersInChat.push(response.data.AddedChatMember);
                    // location.reload()
                }).catch(function (err) {
                    console.log(err);
                    alert("User could not be added to chat.")
                });
            }

        };

    }]);
