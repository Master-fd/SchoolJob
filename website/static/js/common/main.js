/**
 * Created by Administrator on 2016/12/20.
 */

define(function(require){


    window.$ = window.jQuery = require('jquery');  //����jq
    window.pop = require('pop'); //�����ɰ浯��

    var _page = $('#page').data('id');
    switch (_page){

        case 'home' :
        case 'main':
        case 'jobInfo': seajs.use('static/js/home/home.js'); break;   //����Home

        case 'me': seajs.use('static/js/backgroup/backgroup.js');
                    seajs.use('static/js/backgroup/me.js'); break;   //backgroup
        case 'resume':seajs.use('static/js/backgroup/resume.js');
                        seajs.use('static/js/backgroup/backgroup.js'); break;
        case 'applicant':seajs.use('static/js/backgroup/applicant.js');
                    seajs.use('static/js/backgroup/backgroup.js');break;
        case 'collect':seajs.use('static/js/backgroup/backgroup.js');
                    seajs.use('static/js/backgroup/collect.js'); break;
        case 'jobs':seajs.use('static/js/backgroup/backgroup.js');
                    seajs.use('static/js/backgroup/jobs.js'); break;
        case 'organizationResume' : seajs.use('static/js/backgroup/backgroup.js');
                                    seajs.use('static/js/backgroup/organizationResume.js'); break;
    }

    seajs.use('static/js/plugin/bootstrap-3.3.0/dist/js/bootstrap.min.js');
    seajs.use('static/js/common/base.js');   //����header��footer��js
});