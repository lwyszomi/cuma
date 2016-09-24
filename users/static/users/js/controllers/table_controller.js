angular.module('cumaApp').controller('tableController', function($scope, usersConfig, DTDefaultOptions, DTColumnDefBuilder) {
    var vm = this;
    vm.dtOptions = DTDefaultOptions.setDOM('<li<t>p>').setOption('language', {"sLengthMenu":  "_MENU_", 'sInfo': 'of _TOTAL_ users'});
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

    vm.dtColumnDefs = [
        DTColumnDefBuilder.newColumnDef(0),
        DTColumnDefBuilder.newColumnDef(1),
        DTColumnDefBuilder.newColumnDef(2),
        DTColumnDefBuilder.newColumnDef(3),
        DTColumnDefBuilder.newColumnDef(4).notSortable()
    ];

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
                if (table.selectedCountriesTmp.length == 0) {
                    table.redColor = true;
                }
            });
        }
    };
});