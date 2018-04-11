"use strict";

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';')
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i])
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                        break
                    }
                }
            }
            return cookieValue
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))
        }
    }
})

function update(url, id, field, value) {
    $.ajax({
        url: url,
        method: 'post',
        data: {
            id: id,
            field: field,
            value: value
        },
        success: (function () {
            console.log('Updated ' + field + " = " + value + " in #" + id)
        })
    })
}

