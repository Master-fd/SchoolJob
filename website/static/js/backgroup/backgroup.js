/**
 * Created by Administrator on 2016/12/25.
 */
define(function (require, exports) {

    var $body = $('body');
    var $page = $('#page');
    var $pop = $("#pop");
    var pageId = $page.data('id');

/******左侧选项卡*************************************************/
    $body.on('click', '.user-page-left .js-applicant, .user-page-left .js-collect, .user-page-left .js-resume, .user-page-left .js-me', function () {
        var url = resourceUrl+'backgroup/' + $(this).data('id') + '/';
        account.isLoginFun(url);

    });


});