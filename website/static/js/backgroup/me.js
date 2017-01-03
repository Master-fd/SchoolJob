/**
 * Created by Administrator on 2016/11/21.
 */

define(function (require) {

    var $body = $('body');
    var $page = $('#page');
    var $pop = $("#pop");

/********************************个人资料修改处理********************************************************/
    $page.on('click', '.page-containter .modify', function(){
        var $item = $(this).siblings('.nike-name');
        var key = $(this).data('id');
        var title = '';
        if (key == 'password'){
            title = '修改密码';
        }else if(key == 'nickname'){
            title = '修改昵称';
        }else if(key == 'email'){
            title = '修改邮箱'
        }else if(key == 'description'){
            title = '修改描述'
        }


        swal({
            title : title,
            type : 'input',
            showCancelButton : true,
            closeOnConfirm: true,
            confirmButtonText: '确认',
            confirmButtonColor: "rgba(230,69, 102, 1)"
        }, function(data){
            swal.close();
            if (data)
            {
                if (key!='password')
                    $item.text(data);   //如果是密码，则不显示
                account.modifyUserInfo(key, data);
            }
        });
    });

    //显示选择的上传图片
    $page.on('change', '.js-banner-image', function () {
        var file = null;
        var url = null;
        file = $(this)[0].files[0];
        if (window.createObjectURL != undefined) {
            url = window.createObjectURL(file)
        } else if (window.URL != undefined) {
            url = window.URL.createObjectURL(file)
        } else if (window.webkitURL != undefined) {
            url = window.webkitURL.createObjectURL(file)
        }//获取图片的url
        //显示图片
        $(this).siblings('img').attr("src", url);

        //上传
        var data = new FormData();
        data.append('operation', 'uploadBanner');  //上传
        data.append('bannerImageUrl', $page.find("input[name='bannerImageUrl']")[0].files[0]);
        pop.popType('message', '正在上传 . . . . ');
        $.ajax({
            type : "POST",
            url : resourceUrl+"userInfoRequest/",
            data : data,
            cache : false,
            dataType : 'json',
            contentType : false,   //不可缺
            processData : false, //不可缺
            success : function(json_data){
                if (json_data.status == 'success'){
                    pop.popType('success', '上传成功');
                    //location.reload();
                }else{
                    pop.popClose();
                }
            },
            error : function(data){
                pop.popClose();
            }
        });
    });

});