/**
 * Created by Administrator on 2016/12/20.
 */

define(function(require){

    window.$ = window.jQuery = require('jquery');  //����jq
    window.pop = require('pop'); //�����ɰ浯��

    var _page = $('#page').data('id');
    switch (_page){

        case 'home' : seajs.use('static/js/home/home.js'); break;   //����Home
    }

    seajs.use('static/js/common/base.js');   //����header��footer��js
});