angular.module('cumaApp').controller('editController', function($scope, $http, editConfig) {
    vm = this;
    vm.treeOptions = {multiSelection: true};
    vm.dhis_user = editConfig.dhis_user;
    vm.organisationUnits = editConfig.organisationUnits;
    vm.countryLevel = editConfig.countryLevel;
    vm.userGroups = editConfig.userGroups;
    vm.roleUrl = editConfig.roleUrl;
    vm.dataForTree = [];
    vm.selectedNodes = [];
    vm.activeStep = 1;
    vm.organisationsInChunks = [];
    vm.nodeCountries = [];
    vm.newRoles = [];

    vm.splitOrganisation = function() {
        var array = [];
        var orgsCopy = vm.organisationUnits.slice();
        var spliceElements = orgsCopy.length % 3 === 0 ? parseInt(orgsCopy.length/3) : parseInt(orgsCopy.length/3) + 1 ;
        while (orgsCopy.length > 0) {
            array.push([orgsCopy.splice(orgsCopy, spliceElements)])
        }
        vm.organisationsInChunks = array;
    };

    vm.splitOrganisation();

    vm.goToStep = function goToStep(step) {
        vm.activeStep = step;
    };

    vm.addRole = function(item) {
        if (item.role !== void(0) && item.country !== void(0) && item.sector !== void(0)) {
            var role = item.role.selected;
            var country = item.country.selected;
            var sector = item.sector.selected;
            var role_name = role.name + ': ' + country.code + "- " + sector;
            $http({
                url: vm.roleUrl,
                method: "GET",
                params: {"role_name": role_name}
            }).then(function successCallback(response) {
                if (response.data['role'].length > 0) {
                    role = response.data['role'][0];
                    item.show_error = false;
                    vm.newRoles.push(role);
                    item.show_button = true;
                } else {
                    item.show_error = true;
                }
            }, function errorCallback(response) {
            });
        }
    };

    vm.newRole = function(item) {
        item.show_button = false;
        vm.roleForms.push({"show_button": false, "show_error": false})
    };

    vm.removeRole = function (role) {
        var indexInUser = vm.dhis_user.userCredentials.userRoles.indexOf(role);
        var indexInNewRoles = vm.newRoles.indexOf(role);
        if (indexInUser !== -1) {
            vm.dhis_user.userCredentials.userRoles.splice(indexInUser, 1)
        } else if (indexInNewRoles !== -1) {
            vm.newRoles.splice(indexInNewRoles, 1)
        }
    };

    vm.roleForms = [
        {"show_button": false, "show_error": false}
    ];

    // TODO move this to database
    vm.roles = [
        {"name": "Analytics"},
        {"name": "Pivot Table"},
        {"name": "Aggregate Data Entry"},
        {"name": "Individual Data Entry"}
    ];

    vm.findNested = function(obj, key, memo) {
        var i,
            proto = Object.prototype,
            ts = proto.toString,
            hasOwn = proto.hasOwnProperty.bind(obj);

        if ('[object Array]' !== ts.call(memo)) memo = [];

        for (i in obj) {
            if (hasOwn(i)) {
                if (i === 'id' && obj.id === key) {
                    memo.push(obj);
                } else if ('[object Array]' === ts.call(obj[i]) || '[object Object]' === ts.call(obj[i])) {
                    vm.findNested(obj[i], key, memo);
                }
            }
        }

        return memo;
    };

    vm.getCountries = function() {
        var countries = [];
        vm.organisationUnits.forEach(function(ou) {
            var country = {'id': ou.id, 'displayName': ou.displayName, 'code': ou.code, 'sectors': ou.sectors};
            vm.selectedNodes.forEach(function(node) {
                var result = vm.findNested(ou, node.id);
                if (result.length > 0 && countries.indexOf(country) === -1) {
                    countries.push(country)
                }
            })
        });
        vm.nodeCountries = countries;
    };

    vm.getSelectedNodes = function() {
        var nodes = [];
        vm.organisationUnits.forEach(function(ou) {
            vm.dhis_user.organisationUnits.forEach(function(orgs) {
                var result = vm.findNested(ou, orgs.id);
                if (result.length > 0 && nodes.indexOf(orgs) === -1) {
                    nodes.push(result[0])
                }
            })
        });
        vm.selectedNodes = nodes;
        vm.selected = nodes;
    };

    vm.getSelectedNodes();

    $scope.$watchCollection(function() {
        return vm.selectedNodes;
    }, function(newValue, oldValue) {
        if (newValue.length !== oldValue.length) {
            vm.getCountries()
        }
    });

});
