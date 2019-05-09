(function() {

    var app = angular.module('AppChat',['ngRoute']);

    app.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider, $location) {
        $routeProvider.when('/login', {
            templateUrl: 'pages/login.html',
            controller: 'LoginController',
            controllerAs : 'loginCtrl'
        }).when('/chat', {
            templateUrl: 'pages/chat.html',
            controller: 'ChatController',
            controllerAs : 'chatCtrl'
        }).when('/register', {
            templateUrl: 'pages/register.html',
            controller: 'RegisterController',
            controllerAs : 'registerCtrl'

          }).when('/groups', {
            templateUrl: 'pages/group.html',
            controller: 'GroupsController',
            controllerAs : 'groupsCtrl'

           }).when('/joinGroups', {
            templateUrl: 'pages/joinGroup.html',
            controller: 'JoinGroupsController',
            controllerAs : 'joinGroupsCtrl'

        }).otherwise({
            redirectTo: '/chat'
        });
    }]);

})();
