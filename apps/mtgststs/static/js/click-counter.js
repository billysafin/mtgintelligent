$(function($) {
  $('*[href]').addClass('clickable');
  $('li[class="disabled"] > a').attr('disabled', 'disabled').attr('tabindex', '-1').attr('href', 'javascript:void(0)');
});

$(document).on('click', 'a,tr', function(e) {
  if ($(this).hasClass('dropdown-toggle')) {
      return;
  }
  if ($(this).hasClass('non-clickable') || $(this).hasClass('ui-datepicker-prev') || $(this).hasClass('ui-datepicker-next')) {
      return;
  }
  
  //cookie gdpr
  if ($(this).hasClass('cc-btn cc-dismiss') || $(this).hasClass('cc-link')) {
      return;
  }
  
  e.stopPropagation();
  e.preventDefault();
  var href;
  var type;
  var target = $(e.target);
  if(target.is('a') && $(this).hasClass('clickable') && $(this).hasAttr('click-type')){
    href = target.closest('tr').attr('href');
    type = target.closest('tr').attr('click-type');
    //ajax_process(href, type);
  } else if($(this).hasClass('clickable') && $(this).hasAttr('click-type')) {
    if (target.hasAttr('href')) {
      href = target.attr('href');
      type = target.attr('click-type');
    } else {
      href = target.closest('tr').attr('href');
      type = target.closest('tr').attr('click-type');
    }
    //ajax_process(href, type);
  } else if ($(this).hasClass('clickable')) {
    href =  $(this).attr('href');
  }
  
  /* リダイレクト処理 */
  if($(this).attr('header') == 'header') {
   location.href = href;
  } else if(!$(e.target).is('a') && $(this).attr('direction-to') == 'outer-site' && $(this).hasClass('clickable')){
    window.open(href);
  } else if(!$(e.target).is('a') && $(this).attr('direction-to') == 'inner-site' && $(this).hasClass('clickable')) {
    location.href = href;
  } else if($(e.target).is('a') && $(this).hasClass('clickable')) {
      location.href = href;
  } else if($(this).attr('direction-to') == 'outer-site') {
      window.open(href);
  } else if(href !== '' || href !== 'undefined') {
      location.href = href;
  }
  return false;
}).css('cursor','pointer');

function ajax_process(href, type) {
  /* カウント処理 */
  $.ajax({
    type : "POST",
    url : "/click_count",
    data : {
      "href" : href,
      "type" : type
    },
    dataType : "json"
  }).done(function(data, dataType) {
    /*エラーでも処理を継続させたい*/
  }).fail(function(data, dataType) {
    /*エラーでも処理を継続させたい*/
  });
}

$.fn.hasAttr = function(attrName) {
  var result = false;
  if (attrName && attrName !== '') {
    var attrValue = $(this).attr(attrName);
    if (typeof attrValue !== 'undefined' && attrValue !== false) {
      result = true;
    }
  }
  return result;
};
