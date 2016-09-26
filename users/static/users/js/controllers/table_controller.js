angular.module('cumaApp').controller('tableController', function($scope, $filter, usersConfig, DTDefaultOptions,
                                                                 DTOptionsBuilder, DTColumnBuilder) {
    var vm = this;
    vm.dtOptions = DTOptionsBuilder.newOptions()
        .withFnServerData(serverData)
        .withDataProp('data')
        .withOption('processing', true)
        .withOption('serverSide', true)
        .withOption('paging', true);


    DTDefaultOptions
        .setDOM('<li<t>p>')
        .setOption('language', {"sLengthMenu":  "_MENU_", 'sInfo': 'of _TOTAL_ users'});

    vm.allUsers = usersConfig.users;
    vm.users = usersConfig.users;
    vm.countries = usersConfig.countries;


    vm.searchField = "";
    vm.selectedCountries = [];
    vm.selectedUserGroups = [];
    vm.selectedUserRoles = [];
    vm.userGroups = [];
    vm.userRoles = [];
    vm.selectedStatus = {};
    vm.selectedStatus =  {"val": -1, "text": "All"};
    vm.statuses = [
        {"val": -1, "text": "All"},
        {'val': 1, 'text': 'Active'},
        {'val': 0, 'text': 'Inactive'}
    ];
    vm.redColor = false;
    vm.searchFieldTmp = '';
    vm.selectedCountriesTmp = [];
    vm.selectedStatusTmp = {"val": -1, "text": "All"};
    vm.selectedUserGroupsTmp = [];
    vm.selectedUserRolesTmp = [];

    vm.usersFilters = [
        function(array) {
            return $filter('bySearch')(array, vm.searchField);
        },
        function(array) {
            return $filter('byCountry')(array, vm.selectedCountries);
        },
        function(array) {
            return $filter('byUserGroup')(array, vm.selectedUserGroups);
        },
        function(array) {
            return $filter('byUserRoles')(array, vm.selectedUserRoles);
        },
        function(array) {
            return $filter('byStatus')(array, vm.selectedStatus);
        }
    ];

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
        DTColumnBuilder.newColumn('status').withTitle('State'),
        DTColumnBuilder.newColumn('show_url').withTitle('Actions').renderWith(function(data, type, full) {
            return '<a href="' + data + '">Profile</a> | <a href="' + full.edit_url + '">Edit</a>';
        }).notSortable()
    ];

    function serverData(sSource, aoData, fnCallback, oSettings) {
        var draw = aoData[0].value;
        var order = aoData[2].value;
        var start = aoData[3].value;
        var length = aoData[4].value;

        var orderColumn = order[0].column;
        var orderDir = order[0].dir;

        var column = vm.dtColumnDefs[orderColumn].mData;

        var renderFunc = vm.dtColumnDefs[orderColumn].mRender;

        var filteredResults = vm.users;

        vm.usersFilters.forEach(function(filter) {
            filteredResults = filter(filteredResults);
        });

        vm.users.sort(function(x, y) {
            if (renderFunc) {
                x = renderFunc(x[column], null, x);
                y = renderFunc(y[column], null, y);
            } else {
                x = x[column];
                y = y[column];
            }

            if (orderDir == 'asc') {
                return x.localeCompare(y);
            } else {
                return y.localeCompare(x);
            }
        });

        var records = {
            'draw': draw,
            'recordsTotal': vm.users.length,
            'recordsFiltered': filteredResults.length,
            'data': filteredResults.slice(start, start + length)
        };

        fnCallback(records);
    }

    vm.dtInstance = {};

    vm.dtInstanceCallback = dtInstanceCallback;

    function dtInstanceCallback(dtInstance) {
        vm.dtInstance = dtInstance;
    }

    vm.search = function() {
        vm.searchField = vm.searchFieldTmp;
        vm.selectedCountries = vm.selectedCountriesTmp;
        vm.selectedStatus = vm.selectedStatusTmp;
        vm.selectedUserGroups = vm.selectedUserGroupsTmp;
        vm.selectedUserRoles = vm.selectedUserRolesTmp;
        vm.dtInstance.rerender();
    };

    vm.clear = function() {
        vm.searchFieldTmp = '';
        vm.selectedCountriesTmp = [];
        vm.selectedStatusTmp = {"val": -1, "text": "All"};
        vm.selectedUserGroupsTmp = [];
        vm.selectedUserRolesTmp = [];
        vm.searchField = vm.searchFieldTmp;
        vm.selectedCountries = vm.selectedCountriesTmp;
        vm.selectedStatus = vm.selectedStatusTmp;
        vm.selectedUserGroups = vm.selectedUserGroupsTmp;
        vm.selectedUserRoles = vm.selectedUserRolesTmp;
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
                var selectedUserRoles = vm.selectedUserGroups.filter(function(r) {
                    return deletedCountry[0].roles.indexOf(r) === -1;
                });
                vm.selectedUserGroups = vm.selectedUserGroups.filter(function(g) {
                    return deletedCountry[0].groups.indexOf(g) === -1;
                });
                vm.selectedUserRoles = selectedUserRoles;
            }
        }
    });

    vm.setRed = function() {
        if (vm.userGroups.length == 0 && vm.userRoles.length) {
            vm.redColor = true;
        }
    }
}).directive('inputTextClick', function() {
    return {
        restrict: 'A',
        scope: true,
        link: function(scope, element) {
            angular.element(element.find('input')[0]).bind('click', function() {
                var table = scope.$parent.table;
                if (table.filters.selectedCountriesTmp.length == 0) {
                    table.redColor = true;
                }
            });
        }
    };
});