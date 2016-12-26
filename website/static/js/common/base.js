/**
 * Created by Administrator on 2016/11/8.
 */
define(function(require, exports){

    account = require('account');
    school = require('school');


    var $body = $('body'),
        $page = $('#page');


/************导航栏头像login数据*******************/
    //登录头像被点击,
    $body.on('click', '.header .js-login', function(){
         //如果未登陆就弹出登录，已经登陆了就跳转到对应的url
        account.isLoginFun(resourceUrl+'backgroup/home/');
    }).on('click', '.header .js-logout', function () {
        account.logout();  //退出
    }).on('click', '.login-modal .submit-btn', function(){
        //login or goto register
        var userAccount = $(this).siblings("input[name='account']").val();
        var password = $(this).siblings("input[name='password']").val();
        var operation = $(this).data('id');

        if (operation == 'register'){
            //register, 跳转register弹窗
            pop.popClose();
            pop.popType('register');
            school.initSchool('pop-register');   //初始化弹窗数据
            return false;
        }
        if (userAccount.length>15 || userAccount.length<6){
            pop.popType('error', '账户长度6-15字符', '返回修改');
            return false;
        }
        if (password.length>15 || password.length<6){
            pop.popType('error', '密码长度6-15字符', '返回修改');
            return false
        }
        account.login(userAccount, password, operation);
    }).on('click', '.js-register .submit-btn', function () {
        //注册
        var userAccount = $(this).parent().siblings(".modal-content").children("input[name='account']").val();
        var password = $(this).parent().siblings(".modal-content").children("input[name='password']").val();
        var name = $(this).parent().siblings(".modal-content").children("input[name='name']").val();
        var province = school.getProvinceId();//$(this).parent().siblings(".modal-content").find('#js-province option:selected').val();//选中的值
        var university = school.getUniversityId();//$(this).parent().siblings(".modal-content").find('#js-university option:selected').val();//选中的值
        var college = school.getCollegeId();  //$(this).parent().siblings(".modal-content").find('#js-college option:selected').val();//选中的值
        var type = $(this).parent().siblings(".modal-content").find("input[name='js-type']:checked").val();

        if (type=='student'){
            var match = userAccount.match(/^\d+/);
            if (!match){
                pop.popType('error', '学生账户以数字开头', '返回修改');
                return false;
            }
        }
        if (type=='organization'){
            var match = userAccount.match(/^[a-zA-Z]+/);
            if (!match){
                pop.popType('error', '组织账户以字母开头', '返回修改');
                return false;
            }
        }
        if (userAccount.length>15 || userAccount.length<6){
            pop.popType('error', '账户长度6-15字符', '返回修改');
            return false;
        }
        if (password.length>15 || password.length<6){
            pop.popType('error', '密码长度6-15字符', '返回修改');
            return false;
        }
        if (name.length==0){
            pop.popType('error', '学生/组织名不能为空');
            return false;
        }
        if (province == -1){
            pop.popType('error', '省份不能为空');
            return false;
        }
        if (university == -1){
            pop.popType('error', '大学不能为空');
            return false;
        }
        if ((college == -1) && (type=='student')){
            pop.popType('error', '院系不能为空');
            return false;
        }
        data = {
            account : userAccount,
            password : password,
            name : name,
            provinceId : province,
            universityId : university,
            collegeId : college,
            type : type,
            operation : 'register'
        };
        account.register(data);
    }).on('click', '.js-register .cancel-btn', function () {
        //返回
         // 跳转login弹窗
        pop.popClose();
        pop.popType('login');
        return false;
    }).on('click', '.js-change-addr', function () {
        //切换学校
        //弹窗
        pop.popType('address');
        school.initSchool('pop-addr-option');
        return false;
    }).on('click', '.js-addr-option .submit-btn', function () {
        //向服务器设置选定的学校
        pop.popClose();
        var url=resourceUrl+'schoolInfoRequest/';
        var params = {
            operation : 'set',
            provinceId : school.getProvinceId(),
            universityId : school.getUniversityId(),
            collegeId : school.getCollegeId()
        };
        $.post(url, params, function (json_data) {

            if (json_data.status == 'success'){
                //设置显示选定的学校
                var university = json_data.data[1];
                $('.js-change-addr').text(university.name+' | 切换');
            }
        }, 'json');
        return false;
    }).on('click', '.js-addr-option .cancel-btn', function () {
        pop.popClose();
        return false;
    });


});