$( document ).ready(function() {
	$('.dropdown').dropdown();
	$('#rdss_navtop_dropdown')
		.dropdown({
			on: 'hover'
		}) ;
	$('.navtop_rdss_popup') .popup() ;
});
