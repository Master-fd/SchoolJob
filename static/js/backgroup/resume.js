/**
 * Created by Administrator on 2016/12/25.
 */


define(function (require, exports) {

    var $page = $('#page');
    var $body = $('body');
    var url = resourceUrl + 'userInfoRequest/';

    var resumeOtp = {

        //用户添加或修改resume
        addUserResume:function () {
            var name=$body.find('.resume-warp').find("input[name='name']").val();
            var sex=$body.find('.resume-warp').find("input[name='sex']:checked").val();
            var college=$body.find('.resume-warp').find("input[name='college']").val();
            var email=$body.find('.resume-warp').find("input[name='email']").val();
            var phoneNumber=$body.find('.resume-warp').find("input[name='phoneNumber']").val();
            var strong=$body.find('.resume-warp').find("textarea[name='strong']").val();
            var experience=$body.find('.resume-warp').find("textarea[name='experience']").val();
            var others=$body.find('.resume-warp').find("textarea[name='others']").val();
            //合法性判断
            if (!name){
                pop.popType('error', '姓名不能为空');
                return false;
            }
            if (!sex){
                pop.popType('error', '性别不能为空');
                return false;
            }
            if (!college){
                pop.popType('error', '院系不能为空');
                return false;
            }
            if (!email){
                pop.popType('error', 'Email不能为空');
                return false;
            }else{
                match = email.match(/[a-zA-Z0-9]+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+/);
                if (match==null){
                    pop.popType('error', 'Email不合法');
                    return false;
                }
            }
            if (!phoneNumber){
                pop.popType('error', '电话不能为空');
                return false;
            }
            if (!strong){
                pop.popType('error', '特长不能为空');
                return false;
            }
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