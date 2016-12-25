/**
 * Created by Administrator on 2016/12/20.
 */

define(function(require){


    window.$ = window.jQuery = require('jquery');  //加载jq
    window.pop = require('pop'); //加载蒙版弹框

    var _page = $('#page').data('id');
    switch (_page){

        case 'home' : seajs.use('static/js/home/home.js'); break;   //加载Home

        case 'me': seajs.use('static/js/backgroup/backgroup.js');
                    seajs.use('static/js/backgroup/me.js'); break;   //backgroup
        case 'resume':seajs.use('static/js/backgroup/resume.js');
                        seajs.use('static/js/backgroup/backgroup.js'); break;
        case 'applicant':
        case 'collect':seajs.use('static/js/backgroup/backgroup.js'); break;

    }

    seajs.use('static/js/plugin/bootstrap-3.3.0/dist/js/bootstrap.min.js');
    seajs.use('static/js/common/base.js');   //加载header和footer的js
});