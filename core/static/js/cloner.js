/**
 * Created by Rafael on 5/31/2017.
 */

function Cloner(options) {
    this.clone = (function () {
        if (this.counter >= options.maxNumber) {
            return;
        }
        var cloned = $(options.base + ' div.row')
            .clone()
            .removeClass("hidden")
            .appendTo(options.container);
        var select = cloned
            .find('select')
            .attr('id', options.idPrefix + this.counter++);
        if (options.selectUrl) {
            select.select2({
                ajax: {
                    url: options.selectUrl,
                    dataType: 'json',
                    delay: 250,
                    data: function (params) {
                        return {
                            term: params.term,
                            template: options.template
                        }
                    },
                    processResults: function (data) {
                        return {results: data.items};
                    }
                }
            });
        }
        return cloned;
    });
    this.counter = 0;
    $(options.addBtn).on('click', this.clone);
    var parent = this;
    $.get(options.initialUrl)
        .done(function (data) {
            for (var i = 0; i < data.items.length; i++) {
                var cloned = parent.clone();
                if (options.afterLoad) {
                    options.afterLoad(cloned, data.items[i]);
                }
            }
        })
        .always(function () {
            if (options.minNumber) {
                for (; parent.counter < options.minNumber;) {
                    parent.clone();
                }
            }
        });
}