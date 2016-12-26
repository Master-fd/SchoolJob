/**
 * Created by Administrator on 2016/12/25.
 */
define(function (require, exports) {

    var $body = $('body');
    var $page = $('#page');
    var $pop = $("#pop");
    var pageId = $page.data('id');

/******左侧选项卡*************************************************/
    $body.find('.user-page-left').on('click', '.js-applicant, .js-collect, .js-resume, .js-me, .js-jobs', function () {
        var url = resourceUrl+'backgroup/' + $(this).data('id') + '/';
        account.isLoginFun(url);

    });


});