angular.module('cumaApp').factory('ldapUsersService', function($http, jsonUrls) {
    return {
        getUsers: function(searchFilter) {
            var params = {};
            if (searchFilter) {
                params.search = searchFilter
            }
            return $http.get(jsonUrls.ldapUsers, {
                params: params
            }).then(function(response) {
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
