/**
 * Created by arthe on 11/22/2016.
 */

$(document).ready(function() {
    // Clicking on a circle fills all behind and clears all after
    $('.dots input[type=radio]').on('click', function () {
        var val = parseInt($(this).val());
        $(this).siblings().each(function () {
            if ($(this).is('[type=radio]')) {
                $(this).prop('checked', parseInt($(this).val()) <= val);
            } else {
                $(this).val(val);
            }
        });
    });
    // Clicking the clear button empties all circles
    $('.dots button.clear').on('click', function () {
        $(this).siblings().each(function () {
            if ($(this).is('[type=radio]')) {
                $(this).prop('checked', false);
            } else {
                $(this).val(0);
            }
        });
        return false;
    });
    // Click the initial value
    $('.dots').each(function () {
        $(this).children('[type=radio][value="' + $(this).children('[type=hidden]').val() + '"]').click();
    })
});