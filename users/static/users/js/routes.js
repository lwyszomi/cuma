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
});
