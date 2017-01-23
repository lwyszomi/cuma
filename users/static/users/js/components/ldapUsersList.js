angular.module('cumaApp').component('ldapUsersList', {
    templateUrl: function(partialsUrl) {
        return partialsUrl.ldapUsers;
    },
    bindings: {
        users: '<'
    },
    controller: function($scope, $compile, $state, DTOptionsBuilder, DTDefaultOptions, DTColumnBuilder, $q) {
        var vm = this;

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
            DTColumnBuilder.newColumn('mail').withTitle('Name').renderWith(function(data, type, full) {
                var name = [full.sn, full.givenName];
                name = name.filter(function(v) {
                    return angular.isDefined(v);
                });
                return name.join(', ');
            }),
            DTColumnBuilder.newColumn('cn').withTitle('LDAP Identifier'),
            DTColumnBuilder.newColumn('mail').withTitle('Username'),
            DTColumnBuilder.newColumn('mail').withTitle('Actions').renderWith(function(data, type, full) {
                return '<a class="btn btn-primary" href="' + $state.href('users.ldap.edit', {email: full.mail}) + '">Select</a>';
            }).notSortable()
        ];

        function serverData() {
            var deferred = $q.defer();
            deferred.resolve(vm.users);
            return deferred.promise;
        }
    }
});
