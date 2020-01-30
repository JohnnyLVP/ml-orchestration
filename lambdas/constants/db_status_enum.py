from enum import Enum


class DBStatus(str, Enum):
    pending = "PENDING"
    submitted = "SUBMITTED"
    running = "RUNNING"
    completed = "COMPLETED"
    wait = "POLL"
    failed = "FAILED"
    succeeded = "SUCCEEDED"