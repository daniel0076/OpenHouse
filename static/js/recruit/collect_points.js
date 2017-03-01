$( document ).ready(function() {
    $('.ui.dropdown').dropdown();
    $('input[name="card_num"]').focus();
    //on keyup, start the countdown
    //
    var typingTimer;                //timer identifier
    var doneTypingInterval = 100;  //time in ms, 5 second for example
    var $input = $('input[name="card_num"]');
    $input.keyup( function () {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(doneTyping, doneTypingInterval);
    });

    //on keydown, clear the countdown
    $input.keydown( function () {
        clearTimeout(typingTimer);
    });

    //user is "finished typing," do something
    function doneTyping () {
        //do something
        $('#collect_points').submit();
        $('input[name="card_num"]').val('');
    }
});
