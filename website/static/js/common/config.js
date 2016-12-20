/**
 * Created by Administrator on 2016/12/20.
 */


(function (resourceUrl) {

    seajs.config({
        base : resourceUrl,
        alias : {
            'jquery' : 'static/js/plugin/jquery-2.1.4/jquery.js',
            'pop' : 'static/js/common/popmodal.js',
            'account' : 'static/js/common/account.js'
        }
    });

    seajs.use('static/js/common/main.js');  //加载不同的模块

})(resourceUrl);