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
    }).on('click', '.js-sendEmail-btn', function () {
        //弹出发送邮件弹框
        pop.popType('sendEmail');
    }).on('click', '#pop-sendEmail-option .submit-btn', function () {
        //遍历所有选定的resume，发送邮件
        var emailArray = [];
        var url = resourceUrl+'userInfoRequest/';
        var emailContent = $body.find('.email-content').val();
        var checkBox = $body.find("input[name='resume-select']:checked");
        checkBox.each(function (i, n) {
            emailArray.push($(n).data('id'));
        });

        if (!emailArray){
            pop.popType('error', '未选定发送对象');
        }
        if (!emailContent){
            pop.popType('error', 'Email内容不能为空');
        }
        if (resumeIdArray && emailContent){
            var params = {
                operation : 'sendEmail',
                emailArray : emailArray,
                emailContent : emailContent
            };
            $.post(url, params, function (json_data) {
                if (json_data.status=='success'){
                    pop.popType('success', '已发送');
                }else{
                    pop.popType('success', '发送失败');
                }
            }, 'json');
        }
    });

});