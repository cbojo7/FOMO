$(function(context) {
    return function() {
        var container = $('#s1container')
        // $.ajax({
        //     url: 'http://www.byu.edu/',
        
        // })
        // or
        container.load('/catalog/s1demo.inner/')
        console.log(container)
    }
}(DMP_CONTEXT.get()))