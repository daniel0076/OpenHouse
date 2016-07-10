'use strict';
var ctrl = angular.module('oh', []).config(function($interpolateProvider,$httpProvider){
	$interpolateProvider.startSymbol('{$').endSymbol('$}');
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

ctrl.directive('onFinishRender', function ($timeout) {
	return {
		restrict: 'A',
		link: function (scope, element, attr) {
			if (scope.$last === true) {
				$timeout(function () {
					scope.$emit('ngRepeatFinished');
				});
			}
		}
	}
});

ctrl.controller('rdss_select',function($scope, $window,$http,$timeout,$interval,$log) {
	//$scope.load=true;
	//$scope.$on('ngRepeatFinished', function(){
	//	$('.ui.checkbox').checkbox() ;
	//});
	angular.element(document).ready(function () {
		$('.ui.checkbox').checkbox() ;
	});

	var ctrl=this;
	ctrl.selected=null;

	function refresh(){
		$http.post('/rdss/seminar/select_ctrl',{"action":"query"}).success(function(response) {
			ctrl.slot=response.data
		});
	};
	refresh();
	/*
	$interval(function () {
		refresh();
	}, 10000);
	*/

	ctrl.submit=function(){
		$log.log(ctrl.selected);

		var data={};
		data.action = "select";
		data.slot = ctrl.selected;
		$http.post('/rdss/seminar/select_ctrl',data).success(function(response) {
			refresh();
		});
	};

	ctrl.cancel=function(){
		var data={};
		data.action = "cancel";
		$http.post('/rdss/seminar/select_ctrl',data).success(function(response){
			refresh();
		});
	};

});



