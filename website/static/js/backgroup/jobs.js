/**
 * Created by fenton-fd.zhu on 2016/12/26.
 */
define(function (require, exports) {

    var $body = $('body');
    var $pop = $body.find('#pop-add-jobs');
    var url = resourceUrl+'userInfoRequest/';

    $body.on('click', '.js-add-btn', function () {
        //弹窗
        pop.popType('addjob');
    });

    $pop.on('click', '.cancel-btn', function () {
        pop.popClose();
    }).on('click', '.submit-btn', function(){
        var name = $pop.find("input[name='name']").val();
        var department = $pop.find("input[name='department']").val();
        var number = $pop.find("input[name='number']").val();
        var description = $pop.find("textarea[name='description']").val();


        if (!name){
            pop.popType('error', '职位名不能为空');
            return false;
        }
        if (!department){
            pop.popType('error', '部门不能为空');
            return false;
        }
        if (!number){
            pop.popType('error', '数量不能为空');
            return false;
        }
        if (!description){
            pop.popType('error', '描述不能为空');
            return false;
        }
        var params = {
            operation : 'addJob',
            name : name,
            department : department,
            number : number,
            description : description
        };
        $.post(url, params, function (json_data) {
            if (json_data.status=='success'){
                //发布成功
                pop.popClose();
                var data = json_data.data;
                var htmlAttr = [];
                for (var i=0; i<data.length; i++){
                    var htmlStr = [];
                    var foo = data[i];
                    htmlStr.push('<tr data-id='+foo.jobId+'>');
                    htmlStr.push('<td><a href='+foo.url+'>'+foo.name+'</a></td>');
                    htmlStr.push('<td>'+foo.organization+'</td>');
                    htmlStr.push('<td>'+foo.department+'</td>');
                    htmlStr.push('<td>'+foo.number+'</td>');
                    htmlStr.push('<td><a class="js-delete" href="javascript:void (0);">删除</a></td></tr>');
                    htmlAttr.push(htmlStr.join(''));
                }
                console.log(htmlAttr);
                $body.find('.js-job-list').append(htmlAttr.join(''));
            }else{
                pop.popType('error', '发布失败，请重试');
            }
        }, 'json');
    });

    $body.on('click', '.js-job-list .js-delete', function () {
        //删除
        var $this = $(this);
        var jobId = $(this).parents('tr').data('id');
        var params = {
            operation : 'deleteJob',
            jobId : jobId
        };
        $.post(url, params, function (json_data) {

            if (json_data.status == 'success'){
                $this.parents('tr').remove();
            }
        }, 'json');
    });
});