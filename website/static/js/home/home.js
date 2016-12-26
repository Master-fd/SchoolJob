/**
 * Created by Administrator on 2016/12/20.
 */

define(function (require) {

    var $body = $('body');


    $body.on('click', '.job-wrap .js-extend-btn', function () {

        if ($(this).hasClass('up-arrow-icon')){
            $(this).removeClass('up-arrow-icon');
            $(this).addClass('down-arrow-icon');
            //关闭
            $(this).parents('tr').next().addClass('hidden');

        }else {
            $(this).removeClass('down-arrow-icon');
            $(this).addClass('up-arrow-icon');
            //展开
            $(this).parents('tr').next().removeClass('hidden');
        }

    });

});