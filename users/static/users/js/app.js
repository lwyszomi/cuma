var app = angular.module('cumaApp', ['treeControl', 'datatables', 'datatables.bootstrap',
                                     'ui.select', 'ui.router', 'ui.bootstrap', 'ui.keypress']);

app.run(function($rootScope, LoadingOverlayService) {
    var deregisterStateChangeStartHandler = $rootScope.$on('$stateChangeStart', function () {
        LoadingOverlayService.start();
    });

    var deregisterStateChangeEndHandler = $rootScope.$on('$stateChangeSuccess', function () {
        LoadingOverlayService.stop();
    });

    $rootScope.$on('$destroy', function () {
        deregisterStateChangeStartHandler();
        deregisterStateChangeEndHandler();
    });
});
