$(function($) {
  $('#past-search').click(function() {
    $('#past-article–search').toggle();
  }); 
});

$(function($) {
  $('#past-search-small').click(function() {
    $('#past-article–search-small').toggle();
  }); 
});

$(function($) {
  $('#past-search-big').click(function() {
    $('#past-article–search-big').toggle();
  }); 
});

/* 検索div内の言語ーサイト連動  */
$('.lang').change(function() {
  if ($(this).prop('checked')) {
    var selector = '.sites_hidden[country_id="' + $(this).val()  + '"]';
    var site_name;
    var site_id;
    var site_country_id;
    $(selector).each(function() {
      site_name = $(this).attr('site_name');
      site_id = $(this).attr('site_id');
      site_country_id = $(this).attr('country_id');
      $('#sites').append($("<option>").val(site_id).text(site_name).attr('country_id', site_country_id));
    });
  } else {
    var selector = '#sites option[country_id="' + $(this).val() + '"]';  
    $(selector).remove();
  }
});

$('.alignment .btn').click(function() {
  $('#alignment').val($(this).attr('name'));
}); 