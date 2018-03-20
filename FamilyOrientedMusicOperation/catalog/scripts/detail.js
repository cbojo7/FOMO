$(function(){
    $(".thumbnail_list li").on('mouseover',function(){
        url = $( this ).children().attr('src');
        $(".main_image").attr('src', url);
    })
})