(function () {
    $.atoms.job_push_local_files = [
        {
            tag_code: "job_local_files",
            type: "upload",
            attrs: {
                name: gettext("本地文件"),
                hookable: true,
                url: $.context.site_url + 'pipeline/file_upload/' + $.context.biz_cc_id + '/',
                placeholder: gettext("文件名不能包含中文和特殊字符且大小不能超过500M"),
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            },
            methods: {
                handleSuccess: function(response, file, fileList){
                    var file_num = fileList.length;
                    if(response.result){
                        fileList[file_num - 1].time_str = response.time_str;
                    }else{
                        fileList.splice(file_num - 2, 1);
                        show_msg(response.message, 4);
                    }
                    return true;
                },
                handleError: function(err, file, fileList){
                    var result = JSON.parse(err.message)
                    show_msg(result.message, 4);
                }
            }
        },
        {
            tag_code: "job_ip_list",
            type: "textarea",
            attrs: {
                name: gettext("目标IP"),
                placeholder: gettext("IP必须填写【集群名称|模块名称|IP】、【云区域ID:IP】或者【IP】格式之一，多个用换行符分隔；【IP】格式需要保证所填写的内网IP在配置平台(CMDB)的该业务中是唯一的"),
                hookable: true
            }
        },
        {
            tag_code: "job_account",
            type: "input",
            attrs: {
                name: gettext("目标账户"),
                placeholder: gettext("请输入在蓝鲸作业平台上注册的账户名"),
                hookable: true
            }
        },
        {
            tag_code: "job_target_path",
            type: "input",
            attrs: {
                name: gettext("目标路径"),
                placeholder: gettext("请输入绝对路径"),
                hookable: true
            }
        }
    ]
})();