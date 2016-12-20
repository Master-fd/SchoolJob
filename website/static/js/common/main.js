/**
 * Created by Administrator on 2016/12/20.
 */

define(function(require){

    window.$ = window.jQuery = require('jquery');  //加载jq
    window.pop = require('pop'); //加载蒙版弹框

    var _page = $('#page').data('id');
    switch (_page){

        case 'home' : seajs.use('static/js/home/home.js'); break;   //加载Home
    }

    seajs.use('static/js/common/base.js');   //加载header和footer的js
});