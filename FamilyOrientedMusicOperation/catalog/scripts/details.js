$(function(context) {
    return function() {
        var productDetail = $('#product_container')
        right = $('#next_page')
        left = $('#previous_page')
        page = $('#page_number')
        
        right.on('click', function(){
            context.page++
            page.text(context.page)
            container.load("/catalog/index.products/" +context.category_id + "/" + context.page + "/")
        })
        left.on('click', function(){
            context.page--
            page.text(context.page)
            container.load("/catalog/index.products/" +context.category_id + "/" + context.page + "/")
        })

        //container.load('/catalog/index.products/')
        //console.log(container)
    }
}(DMP_CONTEXT.get()))