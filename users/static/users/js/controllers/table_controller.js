angular.module('cumaApp').controller('tableController', function($scope, usersConfig, DTDefaultOptions, DTColumnDefBuilder) {
    var vm = this;
    vm.dtOptions = DTDefaultOptions.setDOM('<l<t>ip>');
    vm.allUsers = usersConfig.users;
    vm.users = usersConfig.users;
    vm.countries = usersConfig.countries;
    vm.searchField = "";
    vm.selectedCountries = [];
    vm.selectedSectors = [];
    vm.selectedUserGroups = [];
    vm.selectedUserRoles = [];
    vm.sectors = [];
    vm.userGroups = [];
    vm.userRoles = [];
    vm.selectedStatus = {};
    vm.selectedStatus =  {"val": -1, "text": "All"};
    vm.statuses = [
        {"val": -1, "text": "All"},
        {'val': 1, 'text': 'Active'},
        {'val': 0, 'text': 'Inactive'}
    ];

    vm.dtColumnDefs = [
        DTColumnDefBuilder.newColumnDef(0),
        DTColumnDefBuilder.newColumnDef(1),
        DTColumnDefBuilder.newColumnDef(2),
        DTColumnDefBuilder.newColumnDef(3).withOption('searchable', false),
        DTColumnDefBuilder.newColumnDef(4).notSortable().withOption('searchable', false)
    ];

    vm.dtInstance = {};

    vm.dtInstanceCallback = dtInstanceCallback;

    function dtInstanceCallback(dtInstance) {
        vm.dtInstance = dtInstance;
    }

    $scope.$watch(function() {
        return vm.searchField;
    }, function(newValue, oldValue) {
        if (newValue !== oldValue) {
            vm.dtInstance.rerender();
        }
    });

    $scope.$watchCollection(function() {
        return vm.selectedCountries;
    }, function(newValue, oldValue) {
        if (newValue.length !== oldValue.length){
            vm.sectors = [];
            vm.userGroups = [];
            vm.userRoles = [];
            newValue.forEach(function (val) {
                vm.sectors.push.apply(vm.sectors, val.children);
                vm.userGroups.push.apply(vm.userGroups, val.groups);
                vm.userRoles.push.apply(vm.userRoles, val.roles);
            });
            var deletedCountry = [];
            deletedCountry = oldValue.filter(function(x) {
                return newValue.indexOf(x) === -1;
            });
            if (deletedCountry.length == 1) {
                var selectedSectors = vm.selectedSectors.filter(function(y) {
                    return deletedCountry[0].children.indexOf(y) === -1;
                });
                var selectedUserGroups = vm.selectedUserGroups.filter(function(g) {
                    return deletedCountry[0].groups.indexOf(g) === -1;
                });
                var selectedUserRoles = vm.selectedUserGroups.filter(function(r) {
                    return deletedCountry[0].roles.indexOf(r) === -1;
                });
                vm.selectedSectors = selectedSectors;
                vm.selectedUserGroups = selectedUserGroups;
                vm.selectedUserRoles = selectedUserRoles;
            }
            vm.dtInstance.rerender();
        }
    });

    $scope.$watchCollection(function() {
        return vm.selectedSectors;
    }, function(newValue, oldValue) {
        if (newValue.length !== oldValue.length) {
            vm.dtInstance.rerender();
        }
    });

    $scope.$watchCollection(function() {
        return vm.selectedUserGroups;
    }, function(newValue, oldValue) {
        if (newValue.length !== oldValue.length) {
            vm.dtInstance.rerender();
        }
    });

    $scope.$watchCollection(function() {
        return vm.selectedUserRoles;
    }, function(newValue, oldValue) {
        if (newValue.length !== oldValue.length) {
            vm.dtInstance.rerender();
        }
    });
    $scope.$watchCollection(function() {
        return vm.selectedStatus;
    }, function(newValue, oldValue) {
        if (newValue !== oldValue) {
            vm.dtInstance.rerender();
        }
    });
});