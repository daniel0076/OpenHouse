
$( document ).ready(function() {
  var slider = new IdealImageSlider.Slider({
    selector: '#slider',
    height: 400, // Required but can be set by CSS
    interval: 3000
  });

  slider.addCaptions();

  $(window).focus(function() {
    slider.start();
  });


  $('.dropdown').dropdown();
  $('#rdss_navtop_dropdown')
    .dropdown({
      on: 'hover'
    })
  ;
});
