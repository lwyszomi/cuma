angular.module('cumaApp').controller('editController', function() {
    this.treeOptions = {multiSelection: true};
    this.dataForTree = [];
    this.selectedNodes = [];
    this.activeStep = 1;

    this.showSelected = function(sel) {
        this.selectedNode = sel;
        var index = this.selectedNodes.indexOf(sel);
        if (index !== -1) {
            this.selectedNodes.splice(index, 1);
        } else {
            this.selectedNodes.push(sel);
        }
     };

    this.goToStep = function goToStep(step) {
        this.activeStep = step;
    }
});
