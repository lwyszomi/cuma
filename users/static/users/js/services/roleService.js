angular.module('cumaApp').factory('roleService', function($http, editConfig) {
    return {
        getRole: function(roleName, countryCode, sector) {
            return $http({
                url: editConfig.roleUrl,
                method: "GET",
                params: {
                    role_name: roleName,
                    country_code: countryCode,
                    sector: sector
                }
            }).then(function(response) {
                return response.data.role;
            });
        }
    }
});
