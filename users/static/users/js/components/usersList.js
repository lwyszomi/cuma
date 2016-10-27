angular.module('cumaApp').component('usersList', {
    bindings: {
        'users': '<',
        'countries': '<',
        'filters': '='
    },
    controller: function($scope, $compile, $http, $q, $state, LoadingOverlayService,
                         DTOptionsBuilder, DTDefaultOptions, DTColumnBuilder, $filter) {
        var vm = this;

        vm.searchFieldTmp = '';
        vm.selectedCountriesTmp = [];
        vm.selectedStatusTmp = {"val": -1, "text": "All"};
        vm.selectedUserGroupsTmp = [];
        vm.selectedUserRolesTmp = [];

        var createdRow = function(row) {
            $compile(angular.element(row).contents())($scope);
        };

        vm.dtOptions = DTOptionsBuilder
            .fromFnPromise(serverData)
            .withDataProp('data')
            .withOption('processing', true)
            .withOption('createdRow', createdRow)
            .withOption('paging', true);

        vm.dtColumnDefs = [
            DTColumnBuilder.newColumn('displayName').withTitle('Name').renderWith(function(data, type, full) {
                 return data + '<br />' + full.roles.length + ' user roles';
            }),
            DTColumnBuilder.newColumn('countries').withTitle('Country').renderWith(function(data) {
                return data.map(function(country) {
                    return country.displayName;
                }).join(' ');
            }),
            DTColumnBuilder.newColumn('username').withTitle('Username'),
            DTColumnBuilder.newColumn('status').withTitle('State').renderWith(function(data, type, full) {
                var oppositeState = '';
                if (data === 'Inactive') {
                    oppositeState = 'Active';
                } else {
                    oppositeState = 'Inactive';
                }
                return data + "<br /><a ng-click='table.changeStatus(\"" + full.id + "\")'>Make " + oppositeState + "</a>"
            }),
            DTColumnBuilder.newColumn('show_url').withTitle('Actions').renderWith(function(data, type, full) {
                var profileUrl = '<a href="' + $state.href('users.profile', {id: full.id}) + '">Profile</a>';
                return profileUrl + ' | ' + '<a href="' + $state.href('users.edit', {id: full.id}) + '">Edit</a>';
            }).notSortable()
        ];

        vm.changeStatus = function(userId) {

            var user = vm.users.filter(function(x) {
                return x.id === userId;
            })[0];

            LoadingOverlayService.start();

            $http.post(user.change_status_url).success(function() {
                var status = user.status;
                if (status === 'Inactive') {
                    user.status = 'Active';
                } else {
                    user.status = 'Inactive';
                }
                vm.dtInstance.reloadData(function() {
                    LoadingOverlayService.stop();
                }, false);
            });
        };

        vm.usersFilters = [
            function(array) {
                return $filter('bySearch')(array, vm.filters.searchField);
            },
            function(array) {
                return $filter('byCountry')(array, vm.filters.selectedCountries);
            },
            function(array) {
                return $filter('byUserGroup')(array, vm.filters.selectedUserGroups);
            },
            function(array) {
                return $filter('byUserRoles')(array, vm.filters.selectedUserRoles);
            },
            function(array) {
                return $filter('byStatus')(array, vm.filters.selectedStatus);
            }
        ];

        function serverData() {

            var deferred = $q.defer();

            var filteredResults = vm.users;

            vm.usersFilters.forEach(function(filter) {
                filteredResults = filter(filteredResults);
            });

            deferred.resolve(filteredResults);
            return deferred.promise;
        }


        DTDefaultOptions
            .setDOM('<li<t>p>')
            .setOption('language', {"sLengthMenu":  "_MENU_", 'sInfo': '&nbsp;&nbsp;of _TOTAL_ users'});

        vm.allUsers = vm.users;

        vm.userGroups = [];
        vm.userRoles = [];

        vm.statuses = [
            {"val": -1, "text": "All"},
            {'val': 1, 'text': 'Active'},
            {'val': 0, 'text': 'Inactive'}
        ];
        vm.redColor = false;

        vm.dtInstance = {};

        vm.dtInstanceCallback = dtInstanceCallback;

        function dtInstanceCallback(dtInstance) {
            vm.dtInstance = dtInstance;
        }

        var assignTmp = function() {
            vm.filters.searchField = vm.searchFieldTmp;
            vm.filters.selectedCountries = vm.selectedCountriesTmp;
            vm.filters.selectedStatus = vm.selectedStatusTmp;
            vm.filters.selectedUserGroups = vm.selectedUserGroupsTmp;
            vm.filters.selectedUserRoles = vm.selectedUserRolesTmp;
        };

        var init = function() {
            vm.searchFieldTmp = vm.filters.searchField;
            vm.selectedCountriesTmp = vm.filters.selectedCountries;
            vm.selectedStatusTmp = vm.filters.selectedStatus;
            vm.selectedUserGroupsTmp = vm.filters.selectedUserGroups;
            vm.selectedUserRolesTmp = vm.filters.selectedUserRoles;

            vm.userRoles = [];
            vm.userGroups = [];
            vm.selectedCountriesTmp.forEach(function (val) {
                vm.userRoles.push.apply(vm.userRoles, val.roles);
                vm.userGroups.push.apply(vm.userGroups, val.groups);
            });
        };

        init();

        vm.search = function() {
            assignTmp();
            vm.dtInstance.reloadData();
        };

        vm.clear = function() {
            vm.searchFieldTmp = '';
            vm.selectedCountriesTmp = [];
            vm.selectedStatusTmp = {"val": -1, "text": "All"};
            vm.selectedUserGroupsTmp = [];
            vm.selectedUserRolesTmp = [];
            vm.filters.searchField = vm.searchFieldTmp;
            vm.filters.selectedCountries = vm.selectedCountriesTmp;
            vm.filters.selectedStatus = vm.selectedStatusTmp;
            vm.filters.selectedUserGroups = vm.selectedUserGroupsTmp;
            vm.filters.selectedUserRoles = vm.selectedUserRolesTmp;
            vm.dtInstance.rerender();
        };

        $scope.$watchCollection(function() {
            return vm.selectedCountriesTmp;
        }, function(newValue, oldValue) {
            if (newValue.length !== oldValue.length){
                vm.redColor = false;
                vm.sectors = [];
                vm.userRoles = [];
                vm.userGroups = [];
                newValue.forEach(function (val) {
                    vm.userRoles.push.apply(vm.userRoles, val.roles);
                    vm.userGroups.push.apply(vm.userGroups, val.groups);
                });
                var deletedCountry = oldValue.filter(function(x) {
                    return newValue.indexOf(x) === -1;
                });
                if (deletedCountry.length == 1) {
                    var rolesId = deletedCountry[0].roles.map(function(x) {
                        return x.id;
                    });

                    var groupsId = deletedCountry[0].groups.map(function(x) {
                        return x.id;
                    });

                    vm.selectedUserRolesTmp = vm.selectedUserRolesTmp.filter(function(r) {
                        return rolesId.indexOf(r.id) === -1;
                    });
                    vm.selectedUserGroupsTmp = vm.selectedUserGroupsTmp.filter(function(g) {
                        return groupsId.indexOf(g.id) === -1;
                    });
                }
            }
        });

        vm.setRed = function() {
            if (vm.userGroups.length == 0 && vm.userRoles.length) {
                vm.redColor = true;
            }
        }
    },
    controllerAs: 'table',
    templateUrl: function(partialsUrl) {
        return partialsUrl.usersList;
    }
}).directive('inputTextClick', function() {
    return {
        restrict: 'A',
        scope: true,
        link: function(scope, element) {
            angular.element(element.find('input')[0]).bind('click', function() {
                var table = scope.$parent.table;
                if (table.selectedCountriesTmp.length == 0) {
                    table.redColor = true;
                }
            });
        }
    };
});
