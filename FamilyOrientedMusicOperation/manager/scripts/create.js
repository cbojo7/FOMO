$(function(){

    var choice = $('#id_title')
    choice.on('change', function(){
        var choice2 = $('#id_title')
            $('#id_max_rental_days').parent().show();
            $('#id_retire_date').parent().show();
            $('#id_quantity').parent().show();
            $('#id_reorder_quantity').parent().show();
            $('#id_reorder_trigger').parent().show();

        if (choice2.val() == 'BulkProduct'){
            $('#id_max_rental_days').parent().hide();
            $('#id_retire_date').parent().hide();
        }
        if (choice2.val() == 'IndividualProduct'){
            $('#id_max_rental_days').parent().hide();
            $('#id_retire_date').parent().hide();
            $('#id_quantity').parent().hide();
            $('#id_reorder_quantity').parent().hide();
            $('#id_reorder_trigger').parent().hide();
        }
        if (choice2.val() == 'RentalProduct'){
            $('#id_quantity').parent().hide();
            $('#id_reorder_quantity').parent().hide();
            $('#id_reorder_trigger').parent().hide();
        }
    }).trigger('change')
})
