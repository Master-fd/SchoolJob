/**
 * Created by Administrator on 2016/11/22.
 */

define(function (require, exports) {

    seajs.use('static/js/plugin/sweetalert/sweetalert.min.js');
    var $body = $('body');

    exports.popType = function (type, title, message, func) {

        switch (type){
            case 'login' : $body.find('.login-modal').css('display', 'block'); break;
            case 'address' : $body.find('.js-addr-option').css('display', 'block'); break;
            case 'register' : $body.find('.js-register').css('display', 'block'); break;
            case 'addjob' : $body.find('.order-modal').css('display', 'block'); break;
            case 'error' : swal({
                               title : title,
                               type : 'error',
                               showCancelButton : false,
                               showConfirmButton : false,
                                timer : 1500
                           }, function(){
                                swal.close();
                                if (func){
                                    func();
                                }
                            });
                break;
            case 'success' : swal({
                               title : title,
                               type : 'success',
                               showCancelButton : false,
                                showConfirmButton : false,
                                timer : 1500
                           }, function(){
                                swal.close();
                                if (func){
                                    func();
                                }
                            });
                break;
            case 'message' : swal({
                               title : title,
                               showCancelButton : false,
                                showConfirmButton : false,
                                timer : 10*60*1000
                           });
                break;
        }
    }

    //代码主动关闭弹窗
    exports.popClose = function(){
        $body.find('#pop-login').css('display', 'none');
        $body.find('#pop-register').css('display', 'none');
        $body.find('#pop-addr-option').css('display', 'none');
    };

    //单击‘x’，或者外面阴影部分，关闭弹窗
    $body.on('click', '.js-modal-close', function(){
        $body.find('#pop-login').css('display', 'none');
        $body.find('#pop-register').css('display', 'none');
        $body.find('#pop-addr-option').css('display', 'none');
    });



});
