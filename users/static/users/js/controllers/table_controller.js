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

    vm.searchFieldTmp = '';
    vm.selectedCountriesTmp = [];
    vm.selectedStatusTmp = {"val": -1, "text": "All"};
    vm.selectedUserGroupsTmp = [];
    vm.selectedUserRolesTmp = [];

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
            vm.sectors = [];
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
            // vm.dtInstance.rerender();
        }
    });
});