$(function () {

    function attachCSVUpload(i, obj) {
        var $dialog = $(obj).find('.csv-upload-dialog'),
            $info = $(obj).find('p.process-info'),
            $uploadBtn = $(obj).find('.upload-btn'),
            $addRow = django.jQuery(obj).find('.add-row a'),
            $fields = $(obj).find('.upload-field'),
            $file = $(obj).find('.csv-file')

        $(obj).find('.module h2').replaceWith($(obj).find('.csv-inline-header'))
        $(obj).on('click', '.csv-upload', function () {
            $dialog.dialog('open')
        })

        $file.on('change', function (ev) {
            $info.text('Preparing data...')
            var reader = new FileReader()
            reader.readAsText(ev.target.files[0])
            reader.onload = function (ev) {
                var data = $.csv.toArrays(ev.target.result)
                $info.text('Prepared ' + data.length +' lines.')
                $uploadBtn
                    .unbind('click')
                    .on('click', function () {
                        $info.text('Transferring data...')
                        var skip = $dialog.find('.skip-check').is(':checked')
                        for (var i=0; i < data.length; i++ ) {
                            if (i===0 && skip) continue
                            $addRow.click()
                            var next = $(obj).find('.form-row').not('.has_original').not('.uploaded').first()
                            $fields.each(function (j, field) {
                                var fieldName = $(field).val()
                                // console.log('Data:' + data[i][j])
                                var $input = next.find('td.field-' + fieldName).find('input.form-control')
                                // console.log($input)
                                if ($input) {
                                    $input.val($.trim(data[i][j]))
                                    next.addClass('uploaded')
                                } else {
                                    console.log('Column error: ' + fieldName)
                                }
                            })
                        }
                        $dialog.dialog('close')
                    })
                    .prop('disabled', false)
            }
            reader.onerror = function (ev) {
                $info.text('Error loading file.')
            }
        })

        $dialog.dialog({
            autoOpen: false,
            modal: true
        })

        $uploadBtn.prop('disabled', true)
    }

    $('.csv-inline').each(attachCSVUpload)

})



