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
        },
        toDHISUser: function(user) {
            return {
                userCredentials: {
                    username: user.mail.toLowerCase(),
                    externalAuth: true,
                    userRoles: [],
                    ldapId: user.cn
                },
                surname: user.sn,
                firstName: user.givenName,
                email: user.mail.toLowerCase(),
                userGroups: [],
                organisationUnits: (user.organisation_unit ? [{id: user.organisation_unit}] : [])
            };
        }
    }
});
