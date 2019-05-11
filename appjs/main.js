(function() {

   var app = angular.module('AppChat', ['ngRoute', 'ngFileUpload']);

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

          }).when('/home', {
            templateUrl: 'pages/home.html',
            controller: 'HomeController',
            controllerAs : 'homeCtrl'

           }).when('/contactlist', {
            templateUrl: 'pages/contactlist.html',
            controller: 'ContactController',
            controllerAs : 'contactCtrl'

             }).when('/dashboard', {
            templateUrl: 'pages/dashboard.html',
            controller: 'DashboardController',
            controllerAs : 'dashboardCtrl'

        }).otherwise({
            redirectTo: '/login'
        });
    }]);




})();
