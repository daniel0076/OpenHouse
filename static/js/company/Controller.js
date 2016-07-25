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

ctrl.controller('company_news',function($scope, $window,$http,$timeout,$interval,$log) {
	//$scope.load=true;
	//$scope.$on('ngRepeatFinished', function(){
	//	$('.ui.checkbox').checkbox() ;
	//});

	var ctrl=this;

	function get_news(){
		$http.post('/company/rdss/seminar/select_ctrl',{"action":"query"}).success(function(response) {
			ctrl.slot = response.data;
			ctrl.select_ctrl = response.select_ctrl;
		});
	};
	get_news();

	ctrl.submit=function(){
	};
});

