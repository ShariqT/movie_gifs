var app = (function(){
	var app = angular.module("app", ["ngRoute"]);
	app.config(["$routeProvider", function($routeProvider){
		$routeProvider.when("/", {
			controller: "SearchController",
			templateUrl: "/static/angular_templates/search.html"
		});
	}]);
	

	var SearchController = function($scope, appTumblrService, appRottenTomatoService){
		$scope.term = "";
		$scope.search = function($event){
			if($event.keyCode == 13){
				startSearch();
			}
		}
		$scope.gifs = null;
		var onSuccess = function(data){
			console.log(data.data.gifs);
			$scope.gifs = data.data.gifs;
		};

		var onError = function(reason){
			console.log(reason);
			$scope.error = reason.data.error;
		}

		var startSearch = function(){
			console.log("starting the search");
			console.log(appTumblrService);
			appTumblrService.searchTags($scope.term).then(onSuccess, onError);
		}

	};

	app.controller('SearchController', SearchController);

	return app;
})();