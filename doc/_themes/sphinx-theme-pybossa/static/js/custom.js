window.onload = function(){

    var header = $('.navbar-default');
    $(window).scroll(function(e){
        if(header.offset().top !== 0){
            if(!header.hasClass('huge')){
                header.addClass('huge');
            }
        }else{
            header.removeClass('huge');
        }
    });
}
