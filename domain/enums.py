from enum import Enum


class LogType(Enum):
    CORE_API_APP = "CoreApiApp"
    CORE_API_ACCESS = "CoreApiAccess"
    USER_FEEDBACK_LIKE_SIM_MOVIE = "UserFeedbackLikeSimilarMovie"
    MOVIE_SIM_MODEL_USED_COUNT = "MovieSimModelUsedCount"

    @classmethod
    def from_value(cls, value: str):
        for e in cls:
            if e.value == value:
                return e
        return None