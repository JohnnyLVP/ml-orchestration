from enum import Enum

class CommonConstants(str, Enum):
    sns_process_filter = "process"
    sns_update_filter = "updates"

    request_succeded = 'REQUESTED'
    request_failed = 'FAILED'
