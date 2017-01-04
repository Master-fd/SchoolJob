/**
 * Created by Administrator on 2016/12/20.
 */

define(function (require) {

    var $body = $('body');

    var searchOption = {

        joinHtml: function (jobList) {

            var htmlAttr = [];
            for (var i=0; i<jobList.length; i++){
                var data = jobList[i];
                var strList=[];
                var strPList = [];
                strList.push('<tr data-id='+data.jobId+'>');
                strList.push('<td><a href='+data.url+'>'+data.name+'</a></td>');
                strList.push('<td>'+data.organization+'</td>');
                strList.push('<td">'+data.department+'</td>');
                strList.push('<td>'+data.number+'</td>');
                strList.push('<td>'+data.updateDate+'<a href="javascript:void (0);" class="js-extend-btn pull-right down-arrow-icon"></a></td></tr>');
                strList.push('<tr class="job-detail hidden">');
                strList.push('<td colspan="5">');
                strList.push('<div>');
                strList.push('<h3>工作职责与要求：</h3>');
                for (var item in data.descriptionLines){
                    strPList.push('<p>--'+item+'</p>');
                }
                strList.push(strPList.join(''));
                strList.push('<div class="job-operation">');
                strList.push('<a class="apply-job" data-index="0">申请职位</a>');
                strList.push('<a class="collect-job" data-index="0">收藏职位</a>');
                strList.push('</div></div></td></tr>');

                htmlAttr.push(strList.join(''));
            };
            $body.find('.job-wrap .js-jobBody').html(htmlAttr.join(''));
        },

        search: function (params) {

            var url = resourceUrl+'searchInfoRequest/';
            $.getJSON(url, params, function (json_data) {

                if (json_data.status=='success'){
                    searchOption.joinHtml(json_data.data);
                }
            });
        }
    };

    var collectOption = {
        //收藏操作
        //添加
        addCollect: function(params) {
            var url = resourceUrl+'userInfoRequest/';
            params['operation'] = 'addCollect';
            $.post(url, params, function (json_data) {

                if (json_data.status == 'success') {
                    pop.popType('success', json_data.message);
                }else{
                    pop.popType('error', json_data.message);
                }
            }, 'json');
        },

    };

    var resumeOption = {
        //发送简历操作
        sendResume: function (params) {
            var url = resourceUrl+'resumeInfoRequest/';
            params['operation'] = 'addUserResume';
            $.post(url, params, function (json_data) {

                if (json_data.status == 'success') {
                    pop.popType('success', json_data.message);
                }else{
                    pop.popType('error', json_data.message);
                }
            }, 'json');
        }
    };

    $body.on('click', '.job-wrap .js-extend-btn', function () {
        //职位详情的显示和关闭
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

    }).on('click', '.js-item', function () {
        //切换选择的组织
        $(this).addClass('current');
        $(this).parents('li').siblings('li').find('a').removeClass('current');
        var oragnizationAccount = $(this).data('id');

        var params = {
            organizationAccount : oragnizationAccount
        };
        searchOption.search(params);

    }).on('click', '.js-search', function () {
        //main 页面搜索
        var name = $(this).siblings('input').val();
        var oragnizationAccount = $(this).parents('div').siblings('div').find('.current').data('id');

        var params = {
            jobName : name,
            organizationAccount : oragnizationAccount
        };
        searchOption.search(params);
    }).on('click', '.collect-job', function () {

        //添加收藏
        var jobId = $(this).parents('tr').prev().data('id');

        if (!jobId){
            jobId = $(this).parents('div').data('id');
        }
        var params = {jobId : jobId};
        collectOption.addCollect(params);
    }).on('click', '.apply-job', function () {
        //发送简历
        var jobId = $(this).parents('tr').prev().data('id');
        if (!jobId){
            jobId = $(this).parents('div').data('id');
        }
        var params = {
            jobId : jobId};
        resumeOption.sendResume(params);
    });




});