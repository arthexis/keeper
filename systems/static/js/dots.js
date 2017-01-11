/**
 * Created by arthe on 11/22/2016.
 */

$(document).ready(function() {
    // Clicking on a circle fills all behind and clears all after
    $(document).on('click', '.dots input[type=radio]', function () {
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
    $(document).on('click', '.dots button.clear', function () {
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
    });
});