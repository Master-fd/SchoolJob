/**
 * Created by Administrator on 2017/1/2.
 */

define(function (require, exports) {

    var $body=$('body');
    var url = resourceUrl+'userDeleteApplicant/';


    $body.on('click', '.js-delete-applicant', function () {
        var $this = $(this);
        var params = {
            operation : 'deleteApplicant',
            applicantId : $this.parents('tr').data('id')
        };
        $.post(url, params, function (json_data) {

            if (json_data.status=='success'){
                $this.parents('tr').remove();
            }
        }, 'json');
    })
});