angular.module('cumaApp').component('ldapUsersList', {
    templateUrl: function(partialsUrl) {
        return partialsUrl.ldapUsers;
    },
    bindings: {
        users: '<'
    },
    controller: function($scope, $compile, $state, DTOptionsBuilder, DTDefaultOptions,
                         DTColumnBuilder, $q, editConfig, LoadingOverlayService, $http, ldapUsersService) {
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
            DTColumnBuilder.newColumn('mail').withTitle('Actions').renderWith(function(data) {
                return '<a class="btn btn-primary" ng-click="$ctrl.save(' + "'" + data + "'" + ')">Select</a>';
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

        vm.$onInit = function() {
            vm.users = filterUsersWithoutName(vm.users);
        };

        vm.clear = function() {
            vm.searchField = '';
            vm.search();
        };

        vm.search = function() {
            LoadingOverlayService.start();
            ldapUsersService.getUsers(vm.searchField).then(function(users) {
                vm.users = filterUsersWithoutName(users);
                vm.dtInstance.reloadData();
            }).finally(function() {
                LoadingOverlayService.stop();
            });
        };

        vm.save = function(userEmail) {
            var user = vm.users.filter(function(u) {
                return u.mail === userEmail;
            })[0];

            var dhisUser = {
                userCredentials: {
                    username: user.mail,
                    externalAuth: true
                },
                surname: user.sn || 'surname',
                firstName: user.givenName || 'firstname',
                email: user.mail,
                ldapId: user.cn
            };

            LoadingOverlayService.start();
            $http.post(editConfig.saveUrl, dhisUser).then(
                function(response) {
                    LoadingOverlayService.stop();
                    var user = response.data;
                    $state.go('users.edit', {id: user.id, step: 1});
                }, function(response) {
                    var errors = response.data.errors;
                    vm.alerts = [];
                    errors.forEach(function(e) {
                        vm.addAlert(e, 'danger');
                    });
                    LoadingOverlayService.stop();
                }
            );
        };

        function serverData() {
            var deferred = $q.defer();
            var users = vm.users;
            deferred.resolve(users);
            return deferred.promise;
        }
    }
});
