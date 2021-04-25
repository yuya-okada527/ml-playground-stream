from typing import List
from domain.log_transformer import CoreApiAccessTransformer, CoreApiAppTransformer, LogTransformer, MovieSimModelUsedCountTransformer, UserFeedbackLikeSimilarMovieTransformer
from enum import Enum
from dataclasses import dataclass

@dataclass(frozen=True)
class LogTypeFields:
    name: str
    transform: LogTransformer
    columns: List[str]
    table_name: str


class LogType(Enum):
    CORE_API_APP = LogTypeFields(
        name="CoreApiApp",
        transform=CoreApiAppTransformer(),
        columns=[
            "level",
            "date_time",
            "file_path",
            "message"
        ],
        table_name="core_api_app_log"
    )
    CORE_API_ACCESS = LogTypeFields(
        name="CoreApiAccess",
        transform=CoreApiAccessTransformer(),
        columns=[
            "date_time",
            "process_time",
            "client_address",
            "method",
            "path",
            "queries",
            "status_code"
        ],
        table_name="core_api_access_log"
    )
    USER_FEEDBACK_LIKE_SIM_MOVIE = LogTypeFields(
        name="UserFeedbackLikeSimilarMovie",
        transform=UserFeedbackLikeSimilarMovieTransformer(),
        columns=[
            "date_time",
            "movie_id",
            "model_type",
            "like"
        ],
        table_name="user_feedback_like_similar_movie"
    )
    MOVIE_SIM_MODEL_USED_COUNT = LogTypeFields(
        name="MovieSimModelUsedCount",
        transform=MovieSimModelUsedCountTransformer(),
        columns=[
            "date_time",
            "model_type"
        ],
        table_name="movie_sim_model_used_count"
    )

    @classmethod
    def from_value(cls, value: str):
        for e in cls:
            if e.value.name == value:
                return e
        return None
