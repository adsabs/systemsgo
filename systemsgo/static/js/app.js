(function() {

  var app = angular.module('ads-services', []);

  app.controller('FrontendController', ['$http', function($http) {

    // Prefill the services for faster loading, and create
    // a name for out of scope filling
    this.services = [];
    frontend = this;

    // Obtain the input from the service end point
    $http.get('http://localhost:5000/status').success(function(data){
      frontend.services = data;
    });

  }]);

})();
