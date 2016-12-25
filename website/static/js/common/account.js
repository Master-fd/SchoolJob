/**
 * Created by Administrator on 2016/11/8.
 */

define(function(require, exports){

    var $page = $('#page');
    var $body = $('body');
    var url = resourceUrl + 'userInfoRequest/';

//    判断是否登录, 设置isLogin, 未登录则弹窗
    exports.isLoginFun = function(successUrl, func){
        //已登录
        if (isLogin){
            if (successUrl){
                window.location.href = successUrl;
                if (func)
                    func();
            }
        }else{
                isLogin = false;
                //    弹窗
                pop.popType('login');
            }
    };
    //登录
    exports.login = function(account, password, operation){
        var params = {
            operation : operation,
            account : account,
            password : password
        };
        pop.popClose();

        $.post(url, params, function(json_data){
            if (json_data.status == 'success'){
                isLogin = true;
                $body.find('.js-logout').css('display' , 'inline-block');
                $body.find('.js-login .js-loginName').text('个人中心');
                //设置显示选定的学校
                var university = json_data.data[1];
                $('.js-change-addr').text(university.name+' | 切换');
            }else{
                pop.popType('error', json_data.message);
            }
        }, 'json');
    };
    //注册
    exports.register = function(data){
        var params = data;
        pop.popClose();

        $.post(url, params, function(json_data){
            if (json_data.status == 'success'){
                isLogin = true;
                pop.popType('success', '注册成功');
                $body.find('.js-logout').css('display' , 'inline-block');
                $body.find('.js-login .js-loginName').text('个人中心');
            }else{
                pop.popType('error', json_data.message);
            }
        }, 'json');
    };
    //退出
    exports.logout = function(){
        var params = {operation : 'logout'};
        $.post(url, params, function(json_data){
            if (json_data.status == 'success'){
                isLogin = false;
                $body.find('.js-logout').css('display' , 'none');
                $body.find('.js-login .js-loginName').text('登录');
                window.location.href = resourceUrl+'home/';
            }
        }, 'json');
    };

//修改用户基本信息
    exports.modifyUserInfo = function (key, value) {

        var params = {
                operation : 'modifyInfo',
            };
        if (key=='nickname')
            params['nickname'] = value;
        if (key=='email')
            params['email'] = value;
        if (key=='password')
            params['password'] = value;

        $.post(url, params, function(json_data){
            if (json_data.status == 'success'){
            }
        }, 'json');
    };



});