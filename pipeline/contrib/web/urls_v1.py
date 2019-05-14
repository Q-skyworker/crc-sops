# -*- coding: utf-8 -*-

from django.conf.urls import url

from pipeline.contrib.web import views_v1

urlpatterns = [
    # 实例操作：启动，暂停，撤销等
    url(r'^act/instances/(?P<action>\w+)/$', views_v1.handle_instance_action),

    # 节点操作：重试，暂停，跳过等
    url(r'^act/nodes/(?P<action>\w+)/$', views_v1.handle_node_action),

    # 查看实例的状态信息
    url(r'^status/$', views_v1.get_state),

    # 获取某个子流程的参数填写表单
    url(r'^form/sub_proc/$', views_v1.get_form_for_subproc),

    # # 获取某个节点重试时的参数填写表单
    # url(r'^form/act_retry/$', views_v1.get_form_for_retry),

    # 获取某个节点的输入和输出
    url(r'^data/act/$', views_v1.get_data_for_activity),

    # 获取某个节点的执行详情
    url(r'^detail/act/$', views_v1.get_detail_for_activity),

    # 获取一个模板的变量列表
    url(r'^data/constants/(?P<template_id>\w+)/$', views_v1.get_constants_for_subproc),

    # 修改实例的输入
    url(r'^inputs/modify/instance/$', views_v1.modify_instance_constants),

    # 克隆一个模板
    url(r'^template/clone/$', views_v1.clone_template),

    # 克隆一个实例
    url(r'^instance/clone/$', views_v1.clone_instance),

    # 重置计时器
    url(r'^spec/timer/reset/$', views_v1.reset_timer),

    # 获取template的context信息
    url(r'^context/template/$', views_v1.get_template_context),

    # 获取instance的context信息
    url(r'^context/instance/$', views_v1.get_instance_context),
]
