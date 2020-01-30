from enum import Enum

class PipelineStages(str, Enum):
	request = "REQUEST"
	algorithm = "ALGORITHM"
	post_process = "POST_PROCESSING"