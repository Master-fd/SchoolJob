/**
 * Created by Administrator on 2016/12/24.
 */


define(function (require, exports) {
    /***********学校数据获取***************************/;
    var $body = $('body');

    var addrOption = {

        //获取省当前id
        getProvinceId: function () {
            return addrOption.htmlParentId.find('#js-province option:selected').val();//选中的值
        },
        //获取学校当前id
        getUniversityId: function(){
            return addrOption.htmlParentId.find('#js-university option:selected').val();//选中的值
        },
        //获取院系当前id
        getCollegeId: function () {
            return addrOption.htmlParentId.find('#js-college option:selected').val();//选中的值
        },

        //联网获取指定数据
        getSchoolData:function (type, func) {

            var url = resourceUrl+'schoolInfoRequest/';
            var params = {
                operation : type,
                provinceId : addrOption.getProvinceId(),
                universityId : addrOption.getUniversityId(),
                collegeId : addrOption.getCollegeId()
            };
            $.getJSON(url, params, function (json_data) {
                if (json_data.status == 'success'){
                    if (func){
                        func(json_data.data);
                    }
                }
            });

        },

        //输出显示option
        postOptions: function (htmlId, data) {
            var htmlAttr = [];
            addrOption.htmlParentId.find(htmlId).empty();  //先清空子节点
            for(var i=0; i<data.length; i++){
                var dic = data[i];
                htmlAttr.push('<option value='+dic.id+'>'+dic.name+'</option>');
            };
            addrOption.htmlParentId.find(htmlId).append(htmlAttr.join(''));
        },

		// 省份option,拼接
		provinceFun:function(func){
            addrOption.getSchoolData('getAllProvinces', function (data){
                //显示省份
                addrOption.postOptions('#js-province', data);
                if (func){
                    func();
                }
            });
		},

		// 学校
		universityFun : function(func){
			addrOption.getSchoolData('getAllUniversity', function (data){
                //显示学校
                addrOption.postOptions('#js-university', data);
                if (func){
                    func();
                }
            });
		},

		// 院/系
		collegeFun : function(func){
            addrOption.getSchoolData('getAllCollege', function (data){
                //显示院系
                addrOption.postOptions('#js-college', data);
                if (func){
                    func();
                }
            });
		}
	};

	// 初始化
	exports.initSchool = function(htmlParentId){

        if (!htmlParentId){
            htmlParentId = '#pop-register';
        }else{
            htmlParentId = '#'+htmlParentId;  //id匹配需要增加#
        }

        addrOption.htmlParentId = $body.find(htmlParentId);

        ////初始化省/校/院
        addrOption.provinceFun(function () {
            addrOption.universityFun(function () {
                addrOption.collegeFun();
            });
        });


        // 绑定单击之后的该变事件
        addrOption.htmlParentId.find('#js-province').on('change',function(){
			addrOption.universityFun(function () {
                addrOption.collegeFun();  //跟着该变
            });

        });

        addrOption.htmlParentId.find('#js-university').on('change', function(){
            addrOption.collegeFun();
		});
	};

    //获取省当前id
    exports.getProvinceId = function () {
        return addrOption.getProvinceId();//选中的值
    };
        //获取学校当前id
    exports.getUniversityId= function(){
            return addrOption.getUniversityId();//选中的值
    };
        //获取院系当前id
    exports.getCollegeId= function () {
            return addrOption.getCollegeId();//选中的值
    }
});