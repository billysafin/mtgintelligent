$('ul.nav.nav-pills li a').click(function() {
  $(this).parent().addClass('active').siblings().removeClass('active');
});

$(function(){
    var topBtn=$('#pageTop');
    topBtn.hide();
    $(window).scroll(function(){
        if($(this).scrollTop()>80){
            topBtn.fadeIn();
        }else{
            topBtn.fadeOut();
        } 
    });
    topBtn.click(function(){
      $('body,html').animate({
      scrollTop: 0},500);
      return false;
    });
});

$(function(){
    $('.expand-side-sites').on('click', function(e){
        var lang = $(this).attr('data-lang');
        $('.side-sites-div').css({'display' : 'none'});
        $('.expand-side-sites span').removeClass("glyphicon glyphicon-triangle-right");
        $('.expand-side-sites span').removeClass("glyphicon glyphicon-triangle-bottom");
        $('.expand-side-sites span').addClass("glyphicon glyphicon-triangle-right");
        $('#' + lang + '-sites').css({'display' : 'block'});
        $('span',this).addClass("glyphicon glyphicon-triangle-bottom");
    });
});

$(function(){
    $('.site-selector').change(function(e){
        var target_form = $(this).attr('data-form');
        $('#' + target_form).submit();
    });
});