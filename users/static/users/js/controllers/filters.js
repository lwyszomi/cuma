angular.module('cumaApp').filter('bySearch', function() {
    return function(items, search) {
        if (search === void(0) || search.length === 0) return items;
        return items.filter(function (item) {
            return (item.displayName.indexOf(search) !== -1 || item.username.indexOf(search) !== -1)
        });

    }
}).filter('byCountry', function() {
    return function(items, selected) {
        var filteredItems = [];
        var countIds = [];
        if (selected === void(0) || selected.length == 0) return items;

        countIds = selected.map(function(item, index) { return item.id});

        items.forEach(function(item) {
            item.countries.forEach(function(country) {
                if (countIds.indexOf(country.id) !== -1 && filteredItems.indexOf(item) === -1) {
                    filteredItems.push(item);
                }
            });
        });
        return filteredItems;
    }
}).filter('bySector', function() {
    return function(items, selected) {
        var filteredItems = [];
        var sectorsIds = [];
        if (selected === void(0) || selected.length == 0) return items;

        sectorsIds = selected.map(function(item, index) { return item.id});

        items.forEach(function(item) {
            item.sectors.forEach(function(sector) {
                if (sectorsIds.indexOf(sector.id) !== -1 && filteredItems.indexOf(item) === -1) {
                    filteredItems.push(item);
                }
            });
        });
        return filteredItems;
    }
}).filter('byUserGroup', function() {
    return function(items, selected) {
        var filteredItems = [];
        var userGroupIds = [];
        if (selected === void(0) || selected.length == 0) return items;

        userGroupIds = selected.map(function(item, index) { return item.id});

        items.forEach(function(item) {
            item.userGroups.forEach(function(group) {
                if (userGroupIds.indexOf(group.id) !== -1 && filteredItems.indexOf(item) === -1) {
                    filteredItems.push(item);
                }
            });
        });
        return filteredItems;
    }
}).filter('byUserRoles', function() {
    return function(items, selected) {
        var filteredItems = [];
        var userRolesIds = [];
        if (selected === void(0) || selected.length == 0) return items;

        userRolesIds = selected.map(function(item, index) { return item.id});

        items.forEach(function(item) {
            item.roles.forEach(function(role) {
                if (userRolesIds.indexOf(role.id) !== -1 && filteredItems.indexOf(item) === -1) {
                    filteredItems.push(item);
                }
            });
        });
        return filteredItems
    }
}).filter('byStatus', function() {
    return function(items, selected) {
        if (selected === void(0) || selected.val === -1) return items;
        return items.filter(function (item, index) { return item.status === selected.text})

    }
});
