from enum import Enum

class CommonConstants(str, Enum):
    sns_process_filter = "process"
    sns_update_filter = "updates"
    dist_search_prefix = "dist" 
    sec_search_prefix = "sec"
    request_succeded = 'REQUESTED'
    request_failed = 'FAILED'
