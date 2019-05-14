# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

# 模板类型
TASK_CATEGORY = (
    ('OpsTools', _(u"运维工具")),
    ('MonitorAlarm', _(u"监控告警")),
    ('ConfManage', _(u"配置管理")),
    ('DevTools', _(u"开发工具")),
    ('EnterpriseIT', _(u"企业IT")),
    ('OfficeApp', _(u"办公应用")),
    ('Other', _(u"其它")),
)

# 任务流程类型
TASK_FLOW_TYPE = [
    ('common', _(u"默认任务流程")),
    ('common_func', _(u"职能化任务流程")),
]

# 任务流程对应的步骤
# NOTE：该变量用于模板和任务授权，如果有变更请务必 makemigrations tasktmpl
TASK_FLOW = {
    'common': [
        ('select_steps', _(u"步骤选择")),  # 创建时即完成该阶段
        ('fill_params', _(u"参数填写")),   # 创建时即完成该阶段
        ('execute_task', _(u"任务执行")),
        ('finished', _(u"完成")),         # 不显示在前端任务流程页面
    ],
    'common_func': [
        ('select_steps', _(u"步骤选择")),  # 创建时即完成该阶段
        ('func_submit', _(u"提交需求")),   # 创建时即完成该阶段
        ('func_claim', _(u"职能化认领")),
        ('execute_task', _(u"任务执行")),
        ('finished', _(u"完成")),         # 不显示在前端任务流程页面
    ]
}


# 任务可操作的类型
TASKENGINE_OPERATE_TYPE = {
    'start_task': 'create',
    'suspend_task': 'pause',
    'resume_task': 'resume',
    'retry_step': 'retry_step_by_id',
    'revoke_task': 'revoke',
    'callback_task': 'callback_task',
    'resume_step': 'resume_step_by_id',
    'complete_step': 'complete_step_by_id',
    'reset_step': 'supersede_step_by_id',
}

# 任务时间类型
TAG_EXECUTE_TIME_TYPES = [
    {"id": 'task_prepare', 'text': _(u"任务准备")},
    {"id": 'doing_work', 'text': _(u"操作执行")},
    {"id": 'db_alter', 'text': _(u"DB变更")},
    {"id": 'db_backup', 'text': _(u"DB备份")},
    {"id": 'online_test', 'text': _(u"现网测试")},
    {"id": 'idle_time', 'text': _(u"空闲时间")},
]

# 通知方式
NOTIFY_TYPE = [
    ("weixin", _(u"微信")),
    ("sms", _(u"短信")),
    ("email", _(u"邮件")),
    ("voice", _(u"语音")),
]
