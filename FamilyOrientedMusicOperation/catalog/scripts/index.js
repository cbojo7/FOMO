$(function(context) {
    return function() {
        var container = $('#product_container')

        container.load('/catalog/index.product/')
        console.log(container)
    }
}(DMP_CONTEXT.get()))