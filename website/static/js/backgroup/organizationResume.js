/**
 * Created by Administrator on 2017/1/2.
 */


define(function (require, exports) {
    var $page = $('#page');
    var $body = $('body');
    var url = resourceUrl + 'userInfoRequest/';

    $body.on('click', '.js-delete-resume', function () {
        $this = $(this);
        //组织筛选删除简历
        var params = {
            operation : 'deleteResume',
            receResumeId : $(this).parents('tr').data('id'),
                jobId : $(this).data('id')
        };
        $.post(url, params, function (json_data) {

            if (json_data.status=='success'){
                $this.parents('tr').remove();
            }
        }, 'json');
    });

});