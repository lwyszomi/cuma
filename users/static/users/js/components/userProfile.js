angular.module('cumaApp').component('userProfile', {
    bindings: {
        'data': '<'
    },
    templateUrl: function(partialsUrl) {
        return partialsUrl.userProfile;
    },
    controller: function($uibModal) {
        var vm = this;
        vm.isObjectEmpty = function(object) {
            return Object.keys(object).length === 0;
        };

        vm.open = function () {
            var modalInstance = $uibModal.open({
                animation: true,
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                templateUrl: 'myModalContent.html',
                controller: function($http, $uibModalInstance, languages, selectedLanguage, saveLanguageUrl) {
                    var vm = this;
                    vm.languages = languages;
                    vm.selectedLanguage = selectedLanguage.code;

                    vm.loading = false;

                    vm.save = function() {
                        vm.loading = true;
                        $http.post(saveLanguageUrl, {language_code: vm.selectedLanguage}).then(function() {
                            vm.loading = false;

                            var selectedLanguage = languages.filter(function(x) {
                                return x.code === vm.selectedLanguage;
                            })[0];

                            $uibModalInstance.close(selectedLanguage);
                        });
                    }
                },
                controllerAs: 'ctrl',
                size: 'sm',
                resolve: {
                    languages: function () {
                        return vm.data.languages;
                    },
                    selectedLanguage: function() {
                        return vm.data.user_language;
                    },
                    saveLanguageUrl: function() {
                        return vm.data.change_language_url;
                    }
                }
            });

            modalInstance.result.then(function(selectedLanguage) {
                debugger;
                vm.data.user_language = selectedLanguage;
            });
        }
    },
    controllerAs: 'ctrl'
});
