angular.module('cumaApp').factory('languagesService', function($http, jsonUrls) {
    return {
        getLanguages: function() {
            return $http.get(jsonUrls.languages).then(function(response) {
                return response.data.languages;
            });
        }
    }
});
