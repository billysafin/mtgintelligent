function ja2Bit (str) {
  return (str.trim().replace(/\s+/g, "").match(/^[a-zA-Z]+$/))? true : false;
}

function simple_tooltip(target_items, name){
 $(target_items).each(function(i){ 
    var title =  $(this).attr('title');
    
    if(title != "" && title != "undefined" ){
      var text = $(this).text();
      if (ja2Bit($(this).text()) === true) {
          title = title.replace('_jp', '_en');
      }
        
      $("body").append("<div style='display:none;' class='"+name+"' id='"+name+i+"'><img src='"+ title +"' /></div>");  
      var my_tooltip = $("#"+name+i); 

      $(this).removeAttr("title").mouseover(function(){
        my_tooltip.css({display:"block"});
        my_tooltip.css({opacity:0.9, display:"none"}).fadeIn(400);  
      }).mousemove(function(kmouse){  
        var border_top = $(window).scrollTop();   
        var border_right = $(window).width();  
        var left_pos;  
        var top_pos;  
        var offset = 20;  
        if(border_right - (offset *2) >= my_tooltip.width() + kmouse.pageX){  
          left_pos = kmouse.pageX+offset;  
        } else{  
          left_pos = border_right-my_tooltip.width()-offset;  
        }  

        if(border_top + (offset *2)>= kmouse.pageY - my_tooltip.height()){  
          top_pos = border_top +offset;  
        } else{  
          top_pos = kmouse.pageY-my_tooltip.height()-offset;  
        }     

        my_tooltip.css({left:left_pos, top:top_pos});  
      }).mouseout(function(){  
        my_tooltip.css({left:"-9999px"});                   
      });  
    }  
  });  
}  