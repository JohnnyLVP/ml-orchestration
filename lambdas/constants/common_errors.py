from enum import Enum

class ErrorCodes(str, Enum):
    # codes for request validation
    failure_internal_server_error = "INTERNAL_SERVER_ERROR"
    failure_invalid_keys = "INVALID_KEYS"
    failure_invalid_json = "INVALID_JSON"
    failure_none = "NONE"

    # codes for etl stage
    cluster_not_found = "NO_EMR_FOUND"
    step_submission_failed = "STEP_SUBMISSION_FAILED"
    proc_timeout = "PROCESS_TIMEOUT"
    proc_exception = "PROCESS_EXCEPTION"

    # codes for post processing stage
    verification_failed = "OUTPUT_VERIFICATION_FAILED"

    # codes for pre etl process and post validation
    pre_processing_failed = "STEP_FUNCTION_TRIGGER_FAILED"