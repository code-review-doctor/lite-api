from audit_trail import service as audit_trail_service
from audit_trail.enums import AuditType

from cases.enums import CaseTypeEnum
from cases.models import Case
from queues.models import Queue
from static.statuses.enums import CaseStatusEnum
from static.statuses.models import CaseStatus
from users.enums import SystemUser
from users.models import GovUser


def get_queues_with_case_assignments(case: Case):
    return set(Queue.objects.filter(case_assignments__case=case).distinct())


def get_next_goods_query_status(case):
    goods_query = case.query.goodsquery
    if (goods_query.clc_responded or not goods_query.clc_raised_reasons) and goods_query.pv_grading_raised_reasons:
        if goods_query.status.status != CaseStatusEnum.PV and not goods_query.status.is_terminal:
            return CaseStatus.objects.get(status=CaseStatusEnum.PV, is_terminal=False)
    return None


def get_next_status_in_workflow_sequence(case):
    if case.case_type.reference == CaseTypeEnum.GOODS.reference:
        return get_next_goods_query_status(case)
    else:
        status = case.status
        if status.workflow_sequence:
            next_status_id = status.workflow_sequence + 1
            try:
                return CaseStatus.objects.get(workflow_sequence=next_status_id, is_terminal=False)
            except CaseStatus.DoesNotExist:
                # If case workflow does have not have a next status
                # Try/catch also verifies that multiple statuses do not exist for a given sequence ID
                pass

        return None


def user_queue_assignment_workflow(queues: [Queue], case: Case):
    from workflow.automation import run_routing_rules

    # Remove case from queues where all gov users are done with the case
    queues_without_case_assignments = set(queues) - get_queues_with_case_assignments(case)
    case.queues.remove(*queues_without_case_assignments)

    system_user = GovUser.objects.get(id=SystemUser.LITE_SYSTEM_ID)

    # This here allows us to look at each queue removed, and assign a countersigning queue for the work queue as needed
    for queue in queues_without_case_assignments:
        if queue.countersigning_queue_id:
            case.queues.add(queue.countersigning_queue_id)
            audit_trail_service.create(
                actor=system_user,
                verb=AuditType.MOVE_CASE,
                action_object=case.get_case(),
                payload={"queues": queue.countersigning_queue.name},
            )

    # Move case to next non-terminal state if unassigned from all queues
    if case.queues.count() == 0:
        next_status = get_next_status_in_workflow_sequence(case)
        if next_status:
            case.status = next_status
            case.save()
            run_routing_rules(case)
