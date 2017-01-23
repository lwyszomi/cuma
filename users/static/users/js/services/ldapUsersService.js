angular.module('cumaApp').factory('ldapUsersService', function($http, jsonUrls) {
    return {
        getUsers: function() {
            return $http.get(jsonUrls.ldapUsers).then(function(response) {
                return response.data.users;
            });
        },
        getUser: function(email) {
            return $http.get(jsonUrls.ldapUser, {
                params: {
                    email: email
                }
            }).then(function(response) {
                return response.data;
            });
        }
    }
});
