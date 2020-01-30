from enum import Enum

class DBTables(str, Enum):
	info = "DY-MLO-ProcessInfo"
	logs = "DY-MLO-NotifProcessingLog"