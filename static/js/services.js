(function(){
	app.factory("appTumblrService", function($http){
		
		var tumblrAPI = "/api/tumblr";
		var t = {};

		t.searchTags = function(term){
			return $http.get(tumblrAPI + "/get_tagged", {params: { "q" : term}}).then(function(data){
				return data;
			});
		}


		return t;
	});



	app.factory("appRottenTomatoService", function($http){
		var rottenTomatoAPI = "/api/rotten";

		var t = {};

		t.queryMovie = function(term){
			return $http.get(rottenTomatoAPI + "/get_movie", {params: {}}).then(function(data){
				return data;
			});
		}

		return t;
	});

})();