$(function () {

    function attachCSVUpload(i, obj) {
        var $dialog = $(obj).find('.csv-upload-dialog')
        $(obj).find('.csv-file').on('change', function () {
            console.log('Uploading')
        })
        $dialog.dialog({
            autoOpen: false,
            modal: true
        })
        $(obj).on('click', '.csv-upload', function () {
            console.log('Test')
            $dialog.dialog('open')
        })
    }

    $('.csv-inline').each(attachCSVUpload)

})



