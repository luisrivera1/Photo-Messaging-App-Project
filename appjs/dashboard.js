angular.module('AppChat').controller('DashboardController', ['$http', '$log', '$scope', '$location', '$routeParams',
    function($http, $log, $scope, $location, $routeParams) {
        var thisCtrl = this;

// Load the Visualization API and the piechart package.
google.charts.load('current', {'packages': ['corechart', 'bar', 'table', 'linechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawHashtagsChart);
google.charts.setOnLoadCallback(drawPostChart);
google.charts.setOnLoadCallback(drawRepliesChart);
google.charts.setOnLoadCallback(drawLikesChart);
google.charts.setOnLoadCallback(drawDislikesChart);
google.charts.setOnLoadCallback(drawActiveUsersChart);
// // google.charts.setOnLoadCallback(drawRepliesPerPostChart);
// google.charts.setOnLoadCallback(drawLikesPerPostChart);
// google.charts.setOnLoadCallback(drawDislikesPerPostChart);

// Hashtags
function reformatHashtagsData(jsonData){
    var temp = jsonData.Trends;
    console.log(temp);
    console.log("temp: " + JSON.stringify(temp));

    var result = [];
    var i;

    for(i=0; i < temp.length && i < 10; i++) {
        dataElement = [];
        dataElement.push(temp[i]["hashtag"]);
        dataElement.push(temp[i]["position"]);
        result.push(dataElement);
    }
    console.log(result);
    return result;
}


function drawHashtagsChart()
{
    var jsonData = $.ajax({
        url: "http://localhost:5000/GramChat/trends",
        dataType: "json",
        async: false
    }).responseText;
    console.log(jsonData);
    console.log("jsonData: " + JSON.parse(jsonData));

    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'hashtag');
    data.addColumn('number', 'position');
    data.addRows(reformatHashtagsData(JSON.parse(jsonData)));

    var options = {
        title: 'Trending Hashtags',
        chartArea: {width: '800px'},
        hAxis: {
            title: 'Trending Hashtags',
            minValue: 0
        },
        vAxis: {
            title: 'Hashtag'
        }
    };
    var chart = new google.visualization.LineChart(document.getElementById('trending_hashtags'));
    chart.draw(data, options);
}

// Post
function reformatPostData(jsonData)
{
    var temp = jsonData.Posts;
    console.log(temp);
    console.log("temp: " + JSON.stringify(temp));
    var result = [];
    var i;
    for(i=0; i < temp.length && i < 10; i++) {
        dataElement = [];
        dataElement.push(temp[i]["day"]);
        dataElement.push(temp[i]["posts"]);
        result.push(dataElement);
    }
    console.log(result);
    return result;
}

function drawPostChart() {
    var jsonData = $.ajax({
        url: "http://localhost:5000/GramChat/postsperday",
        dataType: "json",
        async: false
    }).responseText;
    console.log(jsonData);
    console.log("jsonData: " + JSON.parse(jsonData));

    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Days');
    data.addColumn('number', 'Number of Post');
    data.addRows(reformatPostData(JSON.parse(jsonData)));
    var options = {
        title: 'Posts per day',
        chartArea: {width: '800px'},
        hAxis: {
            title: 'Total Posts',
            minValue: 0
        },
        vAxis: {
            title: 'Day'
        }
    };
    var chart = new google.visualization.LineChart(document.getElementById('postPerDay'));
    chart.draw(data, options);
}

//Replies
function reformatRepliesData(jsonData){
    var temp = jsonData.Posts;
    console.log(temp);
    console.log("temp: " + JSON.stringify(temp));
    var result = [];
    var i;
    for(i=0; i < temp.length && i < 10; i++) {
        dataElement = [];
        dataElement.push(temp[i]["date"]);
        dataElement.push(temp[i]["replies"]);
        result.push(dataElement);
    }
    console.log(result);
    return result;
}

function drawRepliesChart() {
    var jsonData = $.ajax({
        url: "http://localhost:5000/GramChat/replies/date",
        dataType: "json",
        async: false
    }).responseText;
    console.log(jsonData);
    console.log("jsonData: " + JSON.parse(jsonData));
    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Days');
    data.addColumn('number', 'Number of Replies');
    data.addRows(reformatRepliesData(JSON.parse(jsonData)));
    var options = {
        title: 'Replies per day',
        chartArea: {width: '800px'},
        hAxis: {
            title: 'Total Replies',
            minValue: 0
        },
        vAxis: {
            title: 'Day'
        }
    };
    var chart = new google.visualization.LineChart(document.getElementById('repliesPerDay'));
    chart.draw(data, options);
}

//Likes
function reformatLikesData(jsonData){
    var temp = jsonData.Reactions;
    console.log(temp);
    console.log("temp: " + JSON.stringify(temp));

    var result = [];
    var i;

    for(i=0; i < temp.length && i < 10; i++) {
        dataElement = [];
        dataElement.push(temp[i]["date"]);
        dataElement.push(temp[i]["likes"]);
        result.push(dataElement);
    }
    console.log(result);
    return result;
}

function drawLikesChart() {
    var jsonData = $.ajax({
        url: "http://localhost:5000/GramChat/likes/date",
        dataType: "json",
        async: false
    }).responseText;
    console.log(jsonData);
    console.log("jsonData: " + JSON.parse(jsonData));

    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Days');
    data.addColumn('number', 'Number of Likes');
    data.addRows(reformatLikesData(JSON.parse(jsonData)));

    var options = {
        title: 'Likes per day',
        chartArea: {width: '800px'},
        hAxis: {
            title: 'Total Likes',
            minValue: 0
        },
        vAxis: {
            title: 'Day'
        }
    };

    var chart = new google.visualization.LineChart(document.getElementById('likesPerDay'));

    chart.draw(data, options);

}


//Dislikes
function reformatDislikesData(jsonData){
    var temp = jsonData.Reactions;
    console.log(temp);
    console.log("temp: " + JSON.stringify(temp));

    var result = [];
    var i;

    for(i=0; i < temp.length && i < 10; i++) {
        dataElement = [];
        dataElement.push(temp[i]["date"]);
        dataElement.push(temp[i]["dislikes"]);
        result.push(dataElement);
    }
    console.log(result);
    return result;
}


function drawDislikesChart() {
    var jsonData = $.ajax({
        url: "http://localhost:5000/GramChat/dislikes/date",
        dataType: "json",
        async: false
    }).responseText;
    console.log(jsonData);
    console.log("jsonData: " + JSON.parse(jsonData));

    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Days');
    data.addColumn('number', 'Number of Dislikes');
    data.addRows(reformatDislikesData(JSON.parse(jsonData)));

    var options = {
        title: 'Dislikes per day',
        chartArea: {width: '800px'},
        hAxis: {
            title: 'Total Dislikes',
            minValue: 0
        },
        vAxis: {
            title: 'Day'
        }
    };
    var chart = new google.visualization.LineChart(document.getElementById('dislikesPerDay'));
    chart.draw(data, options);
}

function reformatActiveUsersData(jsonData){
    // var temp = jsonData.Active;
    // console.log(temp)
    // console.log("temp: " + JSON.stringify(temp));
    //
    // var result = [];
    // var i;
    //
    // for(i=0; i < temp.length && i < 10; i++) {
    //     dataElement = [];
    //     dataElement.push(temp[i]["username"]);
    //     dataElement.push(temp[i]["total_posts"]);
    //     result.push(dataElement);
    // }
    // console.log(result);
    // return result;
    var temp = jsonData.Activity;
    console.log(temp);
    console.log("temp: " + JSON.stringify(temp));

    var result = [];
    var i;

    for(i=0; i < temp.length && i < 10; i++) {
        dataElement = [];
        dataElement.push(temp[i]["count"]);
        dataElement.push(temp[i]["name"]);    //Creo que tenemos en el primer row el count y el segundo el date. Aqui esta al contrario
        result.push(dataElement);
    }
    console.log(result);
    return result;
}


function drawActiveUsersChart() {
    // var jsonData = $.ajax({
    //     url: "http://localhost:5000/GramChat/users/active",
    //     dataType: "json",
    //     async: false
    // }).responseText;
    // console.log(jsonData);
    // console.log("jsonData: " + JSON.parse(jsonData));
    //
    // Create our data table out of JSON data loaded from server.
    // var data = new google.visualization.DataTable();
    // data.addColumn('string', 'username');
    // data.addColumn('number', 'activity');
    // data.addRows(reformatActiveUsersData(JSON.parse(jsonData)));
    //
    // var options = {
    //     title: 'Top Active Users',
    //     chartArea: {width: '800px'},
    //     hAxis: {
    //         title: 'Top Active Users',
    //         minValue: 0
    //     },
    //     vAxis: {
    //         title: 'Top Active Users'
    //     }
    // };
    // var chart = new google.charts.Bar(document.getElementById('topActiveUsers'));
    // chart.draw(data, options);

    var jsonData = $.ajax({
        url: "http://localhost:5000/GramChat/users/active",
        dataType: "json",
        async: false
    }).responseText;
    console.log(jsonData);
    console.log("jsonData: " + JSON.parse(jsonData));

    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Activities');
    data.addColumn('string', 'Users');
    data.addRows(reformatActiveUsersData(JSON.parse(jsonData)));
    var options = {
        title: 'Top users',
        chartArea: {width: '800px'},
        hAxis: {
            title: 'Users',
            minValue: 0
        },
        vAxis: {
            title: 'Posts'
        }
    };
    var chart = new google.visualization.LineChart(document.getElementById('topUsers'));
    chart.draw(data, options);
}
        this.goHome = function(){
            thisCtrl.uid = $routeParams.uid;
            $location.path('/main/'+$routeParams.uid);
    };
}]);
