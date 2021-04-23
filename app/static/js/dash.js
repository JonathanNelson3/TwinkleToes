$(document).ready(function(){

    $('.state').selectpicker({noneSelectedText: 'N/A'});

    $('.datepicker').datepicker({
        // viewmode: 'years',
        // minviewmode: 'years',
        // format: 'yyyy',
        // autoclose: true,
        // todayHighlight: true,
        // endDate: 'today',
        // autoclose: true,
        // changeYear: true,
        // showButtonPanel: true,
        // maxDate: '@maxDate',
        // minDate: '@minDate',
        // yearRange: "-100:+0",
    });

    $('.datedropdown').datedropdown(number)

    $('.datepicker').datepicker("setDate", new Date());
})