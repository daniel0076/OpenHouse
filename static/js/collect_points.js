$( document ).ready(function() {
    $('.ui.dropdown').dropdown();
    $('input[name="idcard_no"]').focus();

    $('input[name="idcard_no"]').keyup(
            function(){
                if ($('input[name="idcard_no"]').val().length == 10 ) {
                    $('#collect_form').submit();
                    $('input[name="idcard_no"]').val('');
                }
            });
});
