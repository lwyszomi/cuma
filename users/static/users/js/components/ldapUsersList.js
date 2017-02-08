angular.module('cumaApp').component('ldapUsersList', {
    templateUrl: function(partialsUrl) {
        return partialsUrl.ldapUsers;
    },
    bindings: {
        users: '<'
    },
    controller: function($scope, $compile, $state, DTOptionsBuilder, DTDefaultOptions,
                         DTColumnBuilder, $q, editConfig, LoadingOverlayService, $http, ldapUsersService, jsonUrls) {
        var vm = this;

        vm.alerts = [];

        vm.dtInstance = {};

        vm.dtInstanceCallback = dtInstanceCallback;

        function dtInstanceCallback(dtInstance) {
            vm.dtInstance = dtInstance;
        }

        vm.addAlert = function(message, type) {
            vm.alerts.push({type: type, message: message});
        };

        vm.closeAlert = function(index) {
            vm.alerts.splice(index, 1);
        };

        var createdRow = function(row) {
            $compile(angular.element(row).contents())($scope);
        };

        vm.dtOptions = DTOptionsBuilder
            .fromFnPromise(serverData)
            .withDataProp('data')
            .withOption('processing', true)
            .withOption('createdRow', createdRow)
            .withOption('paging', false);

        vm.dtColumnDefs = [
            DTColumnBuilder.newColumn('mail').withTitle('Name').renderWith(function(data, type, full) {
                var name = [full.sn, full.givenName];
                name = name.filter(function(v) {
                    return angular.isDefined(v);
                });
                return name.join(', ');
            }),
            DTColumnBuilder.newColumn('title').withTitle('Title').renderWith(function(data) {
                return data || '';
            }),
            DTColumnBuilder.newColumn('cn').withTitle('LDAP Identifier'),
            DTColumnBuilder.newColumn('mail').withTitle('Username'),
            DTColumnBuilder.newColumn('co').withTitle('Country').renderWith(function(data) {
                return data || '';
            }),
            DTColumnBuilder.newColumn('mail').withTitle('Actions').renderWith(function(data, type, full) {
                return '<a class="btn btn-primary" ng-click="$ctrl.save(' + full.idx + ')">Select</a>';
            }).notSortable()
        ];

        DTDefaultOptions
            .setDOM('<li<t>p>')
            .setOption('language', {"sLengthMenu":  "_MENU_", 'sInfo': ''});

        var filterUsersWithoutName = function(users) {
            return users.filter(function(u) {
                return u.givenName && u.sn && u.mail;
            });
        };

        var addIdxToUsers = function(users) {
            return users.map(function(u, idx) {
                u.idx = idx;
                return u;
            });
        };

        vm.$onInit = function() {
            vm.users = addIdxToUsers(filterUsersWithoutName(vm.users));
        };

        vm.clear = function() {
            vm.searchField = '';
            vm.search();
        };

        var findUser = function(idx) {
            return vm.users.filter(function(u){
                return u.idx === idx;
            })[0];
        };

        vm.search = function() {
            LoadingOverlayService.start();
            ldapUsersService.getUsers(vm.searchField).then(function(users) {
                vm.users = addIdxToUsers(filterUsersWithoutName(users));
                vm.dtInstance.reloadData();
            }).finally(function() {
                LoadingOverlayService.stop();
            });
        };

        vm.save = function(userId) {
            var user = findUser(userId);
            LoadingOverlayService.start();
            $http.get(jsonUrls.userByUsername, {
                params: {
                    username: user.mail
                }
            }).then(function(response) {
                if (response.data.id) {
                    vm.alerts = [];
                    vm.addAlert('User already exists.', 'danger')
                } else {
                    $state.go('users.ldap.editData', {email: user.mail, step: 1});
                }
            }).finally(function() {
                LoadingOverlayService.stop();
            });
        };

        function serverData() {
            var deferred = $q.defer();
            var users = vm.users;
            deferred.resolve(users);
            return deferred.promise;
        }
    }
});
