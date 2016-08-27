 $( document ).ready(function() {
  $('.checkbox').checkbox();
  $('.dropdown').dropdown();
  $('.seminar_clear').click(
	  function(){
		$('.dropdown').dropdown('clear');
	  }
	  );
});
