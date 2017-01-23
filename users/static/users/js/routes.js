angular.module('cumaApp').config(function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/users/');

    $stateProvider
        .state('users', {
            abstract: true,
            controller: function($scope) {
                $scope.filters = {
                    searchField: "",
                    selectedCountries: [],
                    selectedUserGroups: [],
                    selectedUserRoles: [],
                    selectedStatus: {"val": -1, "text": "All"}
                };
            },
            url: '/users',
            template: '<ui-view></ui-view>'
        })
        .state('users.list', {
            url: '/',
            resolve: {
                users: function($http, jsonUrls) {
                    return $http.get(jsonUrls.users).then(function(response) {
                        return response.data.users;
                    });
                },
                countries: function($http, jsonUrls) {
                    return $http.get(jsonUrls.countries).then(function(response) {
                        return response.data.countries;
                    });
                }
            },
            template: '<users-list users="$resolve.users" countries="$resolve.countries" filters="filters"></users-list>'
        })
        .state('users.profile', {
            url: '/profile/{id}',
            resolve: {
                userProfile: function($http, $stateParams, jsonUrls) {
                    return $http.get(jsonUrls.userProfile, {params: {user_id: $stateParams.id}}).then(function(response) {
                        return response.data;
                    });
                }
            },
            template: '<user-profile data="$resolve.userProfile"></user-profile>'
        })
        .state('users.edit', {
            url: '/edit/{id}/{step}',
            resolve: {
                editData: function($http, $stateParams, jsonUrls) {
                    return $http.get(jsonUrls.userEdit, {params: {user_id: $stateParams.id}}).then(function(response) {
                        return response.data;
                    });
                }
            },
            template: function($stateParams) {
                return '<user-edit step="' + $stateParams.step +'" data="$resolve.editData"></user-edit>'
            }
        })
        .state('users.ldap', {
            abstract: true,
            url: '/ldap',
            template: '<ui-view></ui-view>'
        })
        .state('users.ldap.choice', {
            url: '/',
            resolve: {
                users: function($q, $http, jsonUrls, ldapUsersService) {
                    return $q.all([ldapUsersService.getUsers(), $http.get(jsonUrls.users)]).then(function(response) {
                        var ldapUsers = response[0];
                        var dhisUsers = response[1].data.users;

                        var usernamesTaken = dhisUsers.map(function(u) {
                            return u.username;
                        });

                        return ldapUsers.filter(function(ldapUser) {
                            return usernamesTaken.indexOf(ldapUser.mail) === -1;
                        });
                    });
                }
            },
            template: '<ldap-users-list users="$resolve.users"></ldap-users-list>'
        })
        .state('users.ldap.edit', {
            url: '/{email}',
            resolve: {
                user: function(ldapUsersService, $stateParams) {
                    return ldapUsersService.getUser($stateParams.email);
                },
                languages: function(languagesService) {
                    return languagesService.getLanguages();
                }
            },
            template: '<ldap-user-edit user="$resolve.user" languages="$resolve.languages"></ldap-user-edit>'
        });
});
