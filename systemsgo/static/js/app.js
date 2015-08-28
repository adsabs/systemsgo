(function() {

  var app = angular.module('ads-services', []);

  app.controller('FrontendController', ['$interval', '$http', function($interval, $http) {

    // Prefill the services for faster loading, and create
    // a name for out of scope filling
    this.services = [];
    frontend = this;

    // Obtain the input from the service end point
    var getStatus = function() {$http.get('http://adsisdownorjustme.herokuapp.com/status').success(function(data){
      frontend.services = data;
    })};

    $interval(getStatus, 330000);

  }]);

})();
