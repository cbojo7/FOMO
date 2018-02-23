$(function(){
    var choice = $('#id_type')
    choice.on('change', function(){
        var choice2 = $('#id_type')

        if (choice2.val() == 'BulkProduct'){
            $('#id_max_rental_days').parent().hide();
            $('#id_retire_date').parent().hide();
        }
        else if (choice2.val() == 'IndividualProduct'){
            $('#id_max_rental_days').parent().hide();
            $('#id_retire_date').parent().hide();
            $('#id_quantity').parent().hide();
            $('#id_reorder_quantity').parent().hide();
            $('#id_reorder_trigger').parent().hide();
        }
        else if (choice2.val() == 'RentalProduct'){
            $('#id_quantity').parent().hide();
            $('#id_reorder_quantity').parent().hide();
            $('#id_reorder_trigger').parent().hide();
        }
    })
})