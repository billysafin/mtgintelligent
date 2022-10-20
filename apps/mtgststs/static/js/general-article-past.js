$(window).resize(function(){
    var width = window.innerWidth;
    if (width <= 672) {
        $('#past-article–search-big').toggle(false);
    }
    if (width >= 672) {
        $('#past-article–search-small').toggle(false);
    }
  });