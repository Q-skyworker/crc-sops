# -*- coding: utf-8 -*-

import traceback
import logging
import contextlib

from django.db import transaction

from pipeline.engine import signals, states
from pipeline.engine.core.data import get_schedule_parent_data, set_schedule_data, delete_parent_data
from pipeline.engine.models import ScheduleService, Data, Status, PipelineProcess
from pipeline.models import PipelineInstance
from django_signal_valve import valve

logger = logging.getLogger('celery')


@contextlib.contextmanager
def schedule_exception_handler(process_id, schedule_id):
    try:
        yield
    except Exception as e:
        activity_id = schedule_id[:32]
        version = schedule_id[32:]
        if Status.objects.filter(id=activity_id, version=version).exists():
            logger.error(traceback.format_exc(e))
            process = PipelineProcess.objects.get(id=process_id)
            process.exit_gracefully(e)
        else:
            logger.warning('schedule(%s - %s) forced exit.' % (activity_id, version))

        delete_parent_data(schedule_id)


def schedule(process_id, schedule_id):
    """
    调度服务主函数
    :param process_id: 被调度的节点所属的 PipelineProcess
    :param schedule_id: 调度 ID
    :return:
    """
    with schedule_exception_handler(process_id, schedule_id):
        ScheduleService.objects.filter(id=schedule_id).update(is_scheduling=True)
        sched_service = ScheduleService.objects.get(id=schedule_id)
        service_act = sched_service.service_act
        act_id = sched_service.activity_id
        version = sched_service.version

        if not Status.objects.filter(id=act_id, version=version).exists():
            # forced failed
            logger.warning('schedule(%s - %s) forced exit.' % (act_id, version))
            sched_service.destroy()
            return

        # get data
        parent_data = get_schedule_parent_data(sched_service.id)

        # schedule
        ex_data = None
        result = False
        try:
            result = service_act.schedule(parent_data, sched_service.callback_data)
        except Exception as e:
            if service_act.error_ignorable:
                result = True
                service_act.ignore_error()
                service_act.service.finish_schedule()
            else:
                # send activity error signal
                process = PipelineProcess.objects.get(id=sched_service.process_id)
                pipeline_inst = PipelineInstance.objects.get(instance_id=process.root_pipeline_id)
                valve.send(signals, 'activity_failed',
                           sender=process.root_pipeline,
                           pipeline_instance=pipeline_inst,
                           pipeline_activity_id=service_act.id)

            ex_data = traceback.format_exc(e)
            logging.error(ex_data)

        sched_service.schedule_times += 1
        set_schedule_data(sched_service.id, parent_data)

        # schedule failed
        if result is False:
            Data.objects.write_node_data(service_act, ex_data=ex_data)
            if not Status.objects.transit(id=act_id, version=version, to_state=states.FAILED):
                # forced failed
                logger.warning('schedule(%s - %s) forced exit.' % (act_id, version))
                sched_service.destroy()
                return
            process = PipelineProcess.objects.get(id=sched_service.process_id)
            process.adjust_status()

            # send activity error signal
            pipeline_inst = PipelineInstance.objects.get(instance_id=process.root_pipeline_id)
            valve.send(signals, 'activity_failed',
                       sender=process.root_pipeline,
                       pipeline_instance=pipeline_inst,
                       pipeline_activity_id=service_act.id)
            return

        # schedule execute finished or callback finished
        if service_act.schedule_done() or sched_service.wait_callback:
            # write node data and transit status
            Data.objects.write_node_data(service_act)
            if not Status.objects.transit(id=act_id, version=version, to_state=states.FINISHED):
                # forced failed
                logger.warning('schedule(%s - %s) forced exit.' % (act_id, version))
                sched_service.destroy()
                return
            # sync parent data
            with transaction.atomic():
                process = PipelineProcess.objects.select_for_update().get(id=sched_service.process_id)
                if not process.is_alive:
                    logger.warning('schedule(%s - %s) revoked.' % (act_id, version))
                    sched_service.destroy()
                    return

                process.top_pipeline.data.update_outputs(parent_data.get_outputs())
                # extract outputs
                process.top_pipeline.context().extract_output(service_act)
                process.save(save_snapshot=True)

            # clear temp data
            delete_parent_data(sched_service.id)
            # save schedule service
            sched_service.finish()

            valve.send(signals, 'wake_from_schedule',
                       sender=ScheduleService,
                       process_id=sched_service.process_id,
                       activity_id=sched_service.activity_id)
        else:
            sched_service.set_next_schedule()
