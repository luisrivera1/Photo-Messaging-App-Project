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

          }).when('/groups', {
            templateUrl: 'pages/group.html',
            controller: 'GroupsController',
            controllerAs : 'groupsCtrl'

           }).when('/contactlist', {
            templateUrl: 'pages/contactlist.html',
            controller: 'ContactController',
            controllerAs : 'contactCtrl'

             }).when('/dashboard', {
            templateUrl: 'pages/dashboard.html',
            controller: 'DashboardController',
            controllerAs : 'dashboardCtrl'

            }).when('/home', {
            templateUrl: 'pages/home.html',
            controller: 'HomeController',
            controllerAs : 'homeCtrl'


        }).otherwise({
            redirectTo: '/login'
        });
    }]);

   app.directive('ngFile', ['$parse', function ($parse) {
 return {
  restrict: 'A',
  link: function(scope, element, attrs) {
   element.bind('change', function(){

    $parse(attrs.ngFile).assign(scope,element[0].files)
    scope.$apply();
   });
  }
 };
}]);

app.controller('userCtrl', ['$scope', '$http', function ($scope, $http) {

 $scope.upload = function(value){
  var fd=new FormData();
  angular.forEach($scope.uploadfiles,function(file){
  fd.append('file',file);
 });

 $http({
  method: 'post',
  url: '"http://localhost:5000/PhotoMsgApp/posts',
  data: fd,
  headers: {'Content-Type': undefined},
 }).then(function successCallback(response) {
  // Store response data
  $scope.response = response.data;
 });
}

}]);



})();
