import json
import os
from utils.dynamo_db import DBManager
from utils.orchestrator_utils import OrchestratorManager
from constants.db_status_enum import DBStatus
from constants.process_stages_enum import PipelineStages
from constants.common_errors import ErrorCodes
from constants.regular_constants import timestamp_string,process_info, stage, status, created_at, failure_reason, uuid, info, avg_wait_time

def lambda_handler(event, context):

    print(json.dumps(event))
    body = event
    mlo_manager = OrchestratorManager()
    try:
        db_stage, db_status, status_init_time, db_failure_reason = get_current_status_db(
            body)

        if db_status in [DBStatus.succeeded, DBStatus.failed]:
            current_status = db_status
            error_code = db_failure_reason
        elif db_status in [DBStatus.running]:
            total_time_spent_so_far = mlo_manager.get_time_duration(
                status_init_time)
            # time in body in secs.
            if total_time_spent_so_far > body[info][avg_wait_time]*1000:
                print("Total time taken for execution has exceeded the timeout, hence going to stop the execution")
                current_status = DBStatus.failed
                error_code = ErrorCodes.proc_timeout
        else:
            total_time_spent_so_far = mlo_manager.get_time_duration(
                body[info][avg_wait_time])
            if total_time_spent_so_far > 2*60*60*1000:
                print("Total time taken for execution has exceeded the timeout, hence going to stop the execution")
                current_status = DBStatus.failed
                error_code = ErrorCodes.proc_timeout

        body[process_info][stage] = db_stage
        body[process_info][status] = current_status
        body[process_info][created_at] = status_init_time
        body[process_info][failure_reason] = error_code

        return body

    except Exception as e:
        print("Ocurred an exception: {}".format(str(e)))


def get_current_status_db(message):
    dy_processing_table = os.environ['DY_PROCESSING_TABLENAME']
    body = message
    db_manager = DBManager()

    r_stage = None
    r_status = None
    r_created_at = None
    r_failure_reason = None

    try:
        db_item_list = db_manager.get_item_list(
            table_name=dy_processing_table,
            key=uuid,
            value=body[uuid]
        )

        for db_item in db_item_list:
            db_stage = db_item[stage].get('S')
            db_status = db_item[status].get('S')
            db_failure_reason = db_item[failure_reason].get('S')
            created_at = db_item[timestamp_string].get('N')

            if db_stage == PipelineStages.algorithm and db_status in [DBStatus.succeeded, DBStatus.failed]:
                return db_stage, db_status, created_at, db_failure_reason

            if db_stage == PipelineStages.algorithm and db_status in [DBStatus.running]:
                r_stage = db_stage
                r_status = db_status
                r_created_at = created_at
                r_failure_reason = db_failure_reason

        return r_stage, r_status, r_created_at, r_failure_reason

    except Exception as e:
        print("Exception while getting dynamo items: {}".format(str(e)))
