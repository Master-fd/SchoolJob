/**
 * Created by Administrator on 2017/1/2.
 */

define(function (require, exports) {

    var $body= $('body');
    var url = resourceUrl+'userInfoRequest/';

    $body.on('click', '.js-collect-delete', function () {

        var $this = $(this);
        var params = {
            operation : 'deleteCollect',
            collectId : $(this).parents('tr').data('id')
        };

        $.post(url, params, function (json_data) {

            if (json_data.status == 'success'){
                $this.parents('tr').remove();
            }
        }, 'json');

    });
});