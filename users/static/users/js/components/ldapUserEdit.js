angular.module('cumaApp').component('ldapUserEdit', {
    templateUrl: function(partialsUrl) {
        return partialsUrl.ldapUserEdit;
    },
    bindings: {
        user: '<',
        languages: '<'
    },
    controller: function($http, $state, LoadingOverlayService, editConfig) {
        var vm = this;

        vm.$onInit = function() {
            vm.dhisUser = {
                userCredentials: {
                    id: null,
                    username: vm.user.mail,
                    password: 'Default12', // workaround
                    externalAuth: true
                },
                surname: vm.user.sn,
                firstName: vm.user.givenName,
                email: vm.user.mail,
                ldapId: vm.user.cn
            };
        };

        vm.submit = function() {
            LoadingOverlayService.start();
            $http.post(editConfig.saveUrl, vm.dhisUser).then(
                function(response) {
                    LoadingOverlayService.stop();
                    var user = response.data;
                    $state.go('users.edit', {id: user.id, step: 1});
                }, function() {
                    LoadingOverlayService.stop();
                    alert("Unexpected problem");
                }
            );
        };
    }
});
