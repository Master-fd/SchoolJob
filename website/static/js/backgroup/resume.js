/**
 * Created by Administrator on 2016/12/25.
 */


define(function (require, exports) {

    var $page = $('#page');
    var $body = $('body');
    var url = resourceUrl + 'userInfoRequest/';

    var resumeOtp = {

        //添加用户resume
        addUserResume:function () {
            var name=$body.find('.resume-warp').find("input[name='name']").val();
            var sex=$body.find('.resume-warp').find("input[name='sex']:checked").val();
            var college=$body.find('.resume-warp').find("input[name='college']").val();
            var email=$body.find('.resume-warp').find("input[name='email']").val();
            var phoneNumber=$body.find('.resume-warp').find("input[name='phoneNumber']").val();
            var strong=$body.find('.resume-warp').find("textarea[name='strong']").val();
            var experience=$body.find('.resume-warp').find("textarea[name='experience']").val();
            var others=$body.find('.resume-warp').find("textarea[name='others']").val();
            var params = {
                operation : 'addResume',
                name : name,
                sex : sex,
                college : college,
                email : email,
                phoneNumber : phoneNumber,
                strong : strong,
                experience : experience,
                others : others
            };
            $.post(url, params, function (json_data) {

                if (json_data.status == 'success'){
                    pop.popType('success', '修改成功');
                }else{
                    pop.popType('error', '修改失败');
                }
            }, 'json');
        },

    };


    $body.on('click', '.submit-resume-btn', function () {
        resumeOtp.addUserResume();
    });
});