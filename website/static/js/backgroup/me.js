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

});